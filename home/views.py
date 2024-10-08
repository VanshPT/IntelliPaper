from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
import os
import io
import re
import json
from django.conf import settings
from django.urls import reverse
from .models import ResearchPaper, Folder, Readlist, Notes, VectorDocument
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from django.contrib import messages
import google.generativeai as genai
import logging
from sentence_transformers import SentenceTransformer
import numpy as np
from django.contrib.auth.models import User
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import time
import requests
from rank_bm25 import BM25Okapi
from .helper import get_synonyms,get_contextual_terms, get_phrases
import nltk
from django.core.paginator import Paginator
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
#below are imports for running async tasks
from django_q.tasks import async_task



# Set up logging for errors
logger = logging.getLogger(__name__)

# Landing view
def landing(request):
    return render(request, 'home/landing/landing.html')


@login_required
def render_dashboard(request, username):
    user = request.user
    latest_papers = ResearchPaper.objects.filter(user=user).order_by('-upload_datetime')[:8]
    async_task('home.tasks.load_documents')
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'latest_papers': latest_papers
    }
    return render(request, 'home/dashboard_main.html', context)

@login_required
def render_pdf_viewer(request,id):
    if request.user:
        user=request.user
        paper=ResearchPaper.objects.get(id=id)
        context={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'paper':paper
            }
    return render(request, 'home/view_pdf.html', context)


@login_required
def generate_summary(request, id):
    try:
        # Load the paper object using the id (assuming a ResearchPaper model exists)
        paper = ResearchPaper.objects.get(id=id)

        # Use Langchain's PyPDFLoader to load and extract the text from the PDF
        loader = PyPDFLoader(file_path=paper.pdf_file.path)
        pages = loader.load()

        # Combine text from pages into chunks (larger chunks to reduce API calls)
        chunks = [page.page_content for page in pages]

        # Now, configure the Gemini API for processing the chunks
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Define generation configuration for the model
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
            "max_output_tokens": 1500,
            "response_mime_type": "text/plain",
        }

        # Initialize the Gemini model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        # Start a new chat session to maintain context across chunks
        chat_session = model.start_chat(history=[])

        # Throttling and retry parameters
        retry_delay = 5  # Seconds to wait between retries if rate-limited
        max_retries = 5  # Max number of retries after hitting the rate limit

        # Define the prompt template for processing larger combined chunks
        chunk_prompt_template = """
        You are analyzing a research paper. Here is a combined chunk of the paper:
        
        {chunk}

        Please take this chunk into account for your final summary. Do not generate any summary yet.
        """

        def send_with_retry(prompt, retries=0):
            try:
                return chat_session.send_message(prompt)
            except Exception as e:
                if '429' in str(e) and retries < max_retries:
                    logger.warning(f"Rate limit hit. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    return send_with_retry(prompt, retries + 1)
                else:
                    logger.error(f"Error during LLM processing with Gemini: {e}")
                    raise

        # Group chunks into larger batches to minimize the number of API requests
        batch_size = 5  # Increase this number to reduce API calls (experiment with optimal size)
        batched_chunks = [' '.join(chunks[i:i+batch_size]) for i in range(0, len(chunks), batch_size)]

        # Process each batch of chunks
        for batch in batched_chunks:
            try:
                batch_prompt = chunk_prompt_template.format(chunk=batch)
                send_with_retry(batch_prompt)
            except Exception as e:
                return JsonResponse({"error": "An error occurred during batch processing."}, status=500)

        # After all chunks are processed, request a final summary
        summary_prompt = """
        Now that you've seen the entire research article in chunks, please generate a concise summary of the paper.
        """

        # Send the final summary request with retry logic
        final_summary_response = send_with_retry(summary_prompt)

        # Extract the main summary text from the response using regex (optional clean-up)
        raw_summary = final_summary_response.text
        cleaned_summary = re.sub(r'\s+', ' ', raw_summary).strip()

        # Send the cleaned summary as the response to the AJAX request
        return JsonResponse({"summary": cleaned_summary}, status=200)

    except ResearchPaper.DoesNotExist:
        return JsonResponse({"error": "Paper not found"}, status=404)

    except Exception as e:
        logger.error(f"Error in generate_summary view: {e}")
        return JsonResponse({"error": "An error occurred while generating the summary."}, status=500)
    
@login_required
def render_pdf_notes(request,id):
    if request.user:
        user=request.user
        paper=ResearchPaper.objects.get(id=id)
        notes = Notes.objects.filter(user=user, paper=paper).first()
        if notes:
            context={
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'paper':paper,
                'tiny_api': settings.TINY_MCE_EDITOR,
                'notes':notes.content
                }
        else:
            context={
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'paper':paper,
                'tiny_api': settings.TINY_MCE_EDITOR,
                'notes':""
                }
    return render(request, 'home/pdf_notes.html', context)
    

@login_required
def save_notes(request, username, paper_id):
    paper = get_object_or_404(ResearchPaper, id=paper_id)

    if request.method == 'POST':
        user = request.user
        notes_content = request.POST.get('notes')
        notes, created = Notes.objects.get_or_create(user=user, paper=paper)
        notes.content = notes_content
        notes.save()
        return redirect(f'/view_pdf/notes/{paper_id}')

    return redirect(f'/view_pdf/notes/{paper_id}')


@login_required
def render_auto_cluster(request, username):
    user = request.user
    folders=Folder.objects.filter(created_by=user)
    for folder in folders:
        if not folder.papers.exists():
            folder.delete()
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'folders':folders
    }
    return render(request, 'home/auto_clustering.html', context)

@login_required
def render_papers_per_cluster(request, username, id):
    if request.user:
        user=request.user
        folder=Folder.objects.get(created_by=user, id=id)
        context={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'folder':folder
        }
        return render(request, 'home/papers_per_cluster.html', context)
    
    else:
        return render('/authentication/login/')
    
    
@login_required
def render_explore_topics(request, username):
    user = request.user
    research_papers=ResearchPaper.objects.filter(user=user)
    readlists=Readlist.objects.filter(created_by=user)
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'research_papers':research_papers,
        'readlists':readlists
    }
    return render(request, 'home/explore_topics.html', context)

@login_required
def render_papers_per_readlist(request, username, id):
    if request.user:
        user=request.user 
        readlist=Readlist.objects.get(created_by=user, id=id)
        papers=ResearchPaper.objects.filter(user=user)
        context={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'readlist':readlist,
            'papers':papers
        }
        return render(request, 'home/papers_per_readlist.html', context)

@login_required
def render_search_paper(request, username):
    user = request.user
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }
    return render(request, 'home/search_papers.html', context)


@login_required
def render_assistant(request, username):
    user = request.user
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }
    return render(request, 'home/assistant.html', context)

@login_required
def extract_save_pdf(request):
    if request.method == "POST" and request.FILES.get('pdf_file'):
        user = request.user
        pdf_file = request.FILES['pdf_file']
        file_path = default_storage.save(f"data/{pdf_file.name}", pdf_file)
        perm_file_path = default_storage.save(f"pdfs/{pdf_file.name}", pdf_file)
        absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        process_pdf(user,absolute_file_path, pdf_file.name)

        return redirect(f"/dashboard/{user.username}")
    return render(request, 'upload_pdf.html')



def process_pdf(user,pdf_path, pdf_name):
    # Load and chunk the first 5 pages of the PDF
    chunks = chunk_pdf(pdf_path)
    metadata = aggregate_metadata_from_chunks(chunks)
    extracted_text = " ".join([chunk.page_content for chunk in chunks])
    # Saves metadata to the ResearchPaper model
    save_metadata_to_db(user,pdf_name, metadata, extracted_text)

    # this line Deletes the PDF from 'data' folder after processing
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

# Chunk the first 5 pages of the PDF using Langchain
def chunk_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Only take the first 5 pages
    documents = documents[:5]

    # Split the PDF into manageable chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)  # Adjust chunk size to 1500 tokens
    chunks = splitter.split_documents(documents)

    return chunks
logger = logging.getLogger(__name__)

# Use Gemini to extract metadata from chunks
def aggregate_metadata_from_chunks(chunks):
    # Configure Gemini API key from environment
    genai.configure(api_key=settings.GEMINI_API_KEY)

    # Define generation configuration for the model
    generation_config = {
        "temperature": 0.0,  # For more deterministic responses
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the Gemini model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Start a new chat session
    chat_session = model.start_chat(history=[])

    # Initialize metadata dictionary
    metadata = {"title": "", "authors": "", "abstract": ""}

    # Aggregate responses from all chunks
    all_responses = []

    # Define the LLM prompt
    prompt_template = """
    Extract the title, author, and abstract(complete) from the following chunk of a PDF(dont give any formattings (like **title** for example, give directly title)):

    {chunk}

    Respond in the format:
    - Title: __
    - Authors: __
    - Abstract: __
    """

    for chunk in chunks:
        try:
            # Prepare the prompt for the current chunk
            prompt = prompt_template.format(chunk=chunk.page_content)

            # Send the prompt to Gemini API and receive the response
            response = chat_session.send_message(prompt)

            # Append the response to aggregate all chunks
            all_responses.append(response.text)

        except Exception as e:
            logger.error(f"Error during LLM processing with Gemini: {e}")

    # Combine all responses into a single string
    combined_response = " ".join(all_responses)

    # Use regex to extract metadata
    metadata["title"] = re.search(r"Title:\s*(.*)", combined_response).group(1) if re.search(r"Title:\s*(.*)", combined_response) else ""
    metadata["authors"] = re.search(r"Authors:\s*(.*)", combined_response).group(1) if re.search(r"Authors:\s*(.*)", combined_response) else ""
    metadata["abstract"] = re.search(r"Abstract:\s*(.*)", combined_response).group(1) if re.search(r"Abstract:\s*(.*)", combined_response) else ""
    print(metadata)
    return metadata

def trigger_auto_clustering(username):
    # Build the URL for the auto_cluster API
    auto_cluster_url = reverse('auto_cluster', args=[username])
    full_url = f'{settings.BASE_URL}{auto_cluster_url}'
    
    # Call the auto_cluster API using a GET request
    try:
        response = requests.get(full_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            print(f"Auto-clustering for user {username} triggered successfully.")
        else:
            print(f"Failed to trigger auto-clustering. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error during auto-clustering API request: {e}")

# Function to save the metadata and trigger auto-clustering after a delay
def save_metadata_to_db(user, pdf_name, metadata, extracted_text):
    # Get the user instance
    user_instance = User.objects.get(username=user.username)

    # Save the research paper
    paper = ResearchPaper(
        user=user_instance,
        title=metadata["title"],
        authors=metadata["authors"],
        abstract=metadata["abstract"],
        pdf_file=f'pdfs/{pdf_name}',
        extracted_text=extracted_text
    )
    paper.save()

    
@login_required
def delete_paper(request, username, id):
    if request.user.username != username:
        return redirect('/login/')
    paper = get_object_or_404(ResearchPaper, id=id, user=request.user)
    pdf_path = os.path.join(settings.MEDIA_ROOT, str(paper.pdf_file))
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    folders_with_paper = paper.folders.all()
    paper.delete()
    for folder in folders_with_paper:
        if not folder.papers.exists():
            folder.delete()
    return redirect(f'/dashboard/{username}')


@login_required
def delete_paper1(request, username, id):
    if request.user.username != username:
        return redirect('/login/')
    paper = get_object_or_404(ResearchPaper, id=id, user=request.user)
    pdf_path = os.path.join(settings.MEDIA_ROOT, str(paper.pdf_file))
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    folders_with_paper = paper.folders.all()
    paper.delete()
    for folder in folders_with_paper:
        if not folder.papers.exists():
            folder.delete()
    return redirect(f'/explore_topics/{username}')


@login_required
def auto_cluster(request, username):
    if request.user.username !=username:
        messages.error(request, "You are not logged in with this username")
        return redirect('/')
    papers = ResearchPaper.objects.filter(user=request.user)
    if papers.count() == 0:
        messages.info(request, "No PDFs exist in your account.")
        return redirect(f'/auto_cluster/{username}')
    if papers.count() == 1:
        messages.info(request, "Only one paper exists in your account.")
        return redirect(f'/auto_cluster/{username}')
    
    embeddings, paper_ids = get_embeddings_for_papers(papers)
    cluster_labels = perform_clustering(embeddings)
    cluster_names = get_cluster_names(cluster_labels, len(set(cluster_labels)), paper_ids, papers)
    save_clusters(cluster_names, cluster_labels, paper_ids, request.user)
    
    return redirect(f'/auto_cluster/{request.user.username}')



def get_embeddings_for_papers(papers):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # BERT-like embeddings
    embeddings = []
    paper_ids = []

    for paper in papers:
        text = paper.extracted_text[:5000]
        embedding = model.encode(text, convert_to_numpy=True)
        embeddings.append(embedding)
        paper_ids.append(paper.id)

    return np.array(embeddings), paper_ids




media_dir = 'media/agg_models'
os.makedirs(media_dir, exist_ok=True)
def perform_clustering(embeddings):
    # Compute cosine similarity matrix for embeddings
    similarity_matrix = cosine_similarity(embeddings)
    
    clustering_model = AgglomerativeClustering(
        metric='precomputed',
        linkage='average',
        distance_threshold=0.5,
        n_clusters=None
    )
    cluster_labels = clustering_model.fit_predict(1 - similarity_matrix)
    model_path = os.path.join(media_dir, 'agglomerative_clustering_model.joblib')
    joblib.dump(clustering_model, model_path)

    return cluster_labels


def get_cluster_names(cluster_labels, n_clusters, paper_ids, papers):
    # Configure Gemini API key
    genai.configure(api_key=settings.GEMINI_API_KEY)

    # Define generation configuration
    generation_config = {
        "temperature": 0.0,  # More deterministic responses
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 100,  # Limit tokens to avoid resource issues
        "response_mime_type": "text/plain",
    }

    # Initialize the Gemini model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Start a new chat session (reuse this for all requests)
    chat_session = model.start_chat(history=[])

    cluster_names = {}
    prompt_template = """
    Based on the following paper excerpts, provide a meaningful folder name that categorizes them, if clusters have multiple topics like AI and Business finance etc, then folder name should be Ai, Business Finance. give clean folder names which are crisp and small based on understanding of cluster. Keep the title in normal font in response dont add **TITLE**, just output TITLE.Only give directly the answer nothing else before or after.
    Text excerpts: 
    {paper_excerpts}
    """

    all_responses = []

    for cluster in range(n_clusters):
        # Get papers in this cluster
        papers_in_cluster = [papers.get(id=paper_ids[i]) for i in range(len(paper_ids)) if cluster_labels[i] == cluster]

        # Extract text excerpts from each paper, but limit the total size to avoid long prompts
        paper_texts = [paper.extracted_text[:300] for paper in papers_in_cluster]  # Limit excerpt size to 300 chars per paper
        paper_excerpts = " ".join(paper_texts)
        print(paper_excerpts)
        if not paper_excerpts.strip():  # If no excerpts, skip to next cluster
            cluster_names[cluster] = f"Cluster_{cluster}"
            continue

        # Create the prompt
        prompt = prompt_template.format(paper_excerpts=paper_excerpts)

        try:
            # Send the prompt to Gemini and get the response
            response = chat_session.send_message(prompt)
            cluster_names[cluster] = response.text.strip()
            
            # Sleep for 3 seconds after receiving the response
            # time.sleep(10)

        except Exception as e:
            logging.error(f"Error during LLM processing with Gemini: {e}")
            # Fallback to a default cluster name if there's an error
            cluster_names[cluster] = f"Cluster_{cluster}"

    return cluster_names



def save_clusters(cluster_names, cluster_labels, paper_ids, user):
    # Delete all existing folders for this user before creating new clusters
    Folder.objects.filter(created_by=user).delete()

    for cluster, folder_name in cluster_names.items():
        folder = Folder.objects.create(name=folder_name, created_by=user)

        papers_in_cluster = [paper_ids[i] for i in range(len(paper_ids)) if cluster_labels[i] == cluster]
        folder.papers.set(ResearchPaper.objects.filter(id__in=papers_in_cluster))
        folder.save()


@csrf_exempt  # Use cautiously; consider adding CSRF token handling for security
@login_required  # Ensure the user is authenticated
def rename_readlist(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            old_name = data.get('oldName')
            new_name = data.get('newName')
            user = request.user

            # Check if the readlist with old_name exists
            try:
                readlist = Readlist.objects.get(name=old_name, created_by=user)
                # Check if the new_name already exists
                if Readlist.objects.filter(name=new_name, created_by=user).exists():
                    return JsonResponse({'success': False, 'message': f'There is already a readlist named "{new_name}" in your account.'}, status=400)

                # Update the name
                readlist.name = new_name
                readlist.save()
                return JsonResponse({'success': True, 'message': 'Readlist renamed successfully.'})

            except Readlist.DoesNotExist:
                # Create a new readlist with the new_name if old_name doesn't exist
                if not Readlist.objects.filter(name=new_name, created_by=user).exists():
                    Readlist.objects.create(name=new_name, created_by=user)
                    return JsonResponse({'success': True, 'message': 'New readlist created successfully.'})
                else:
                    return JsonResponse({'success': False, 'message': f'There is already a readlist named "{new_name}" in your account.'}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

@login_required
def save_papers_to_readlist(request, username):
    if request.method == 'POST':
        logger.info("View has been called.")
        user = request.user
        readlist_id = request.POST.get('readlist_id')
        readlist = get_object_or_404(Readlist, id=readlist_id, created_by=request.user)

        # Get the selected paper IDs from the form
        paper_ids = request.POST.getlist('papers')

        if not paper_ids:
            messages.error(request, "No papers selected. Please select at least one paper.")
            return redirect(f'/explore_topics/{user.username}')

        # Filter papers that are already in the readlist
        existing_papers = readlist.papers.filter(id__in=paper_ids).values_list('id', flat=True)
        new_papers_ids = [paper_id for paper_id in paper_ids if int(paper_id) not in existing_papers]

        if not new_papers_ids:
            messages.error(request, "All selected papers are already in this readlist.")
            return redirect(f'/explore_topics/{user.username}/{readlist_id}/')

        # If some papers are already in the readlist, show an error for those and add the new ones
        if existing_papers:
            messages.error(request, f"Some papers are already in this readlist: {', '.join(map(str, existing_papers))}.")
        
        # Add only new papers to the readlist
        papers_to_add = ResearchPaper.objects.filter(id__in=new_papers_ids)
        readlist.papers.add(*papers_to_add)

        if new_papers_ids:
            messages.success(request, "Papers added to the readlist successfully!")

        return redirect(f'/explore_topics/{user.username}/{readlist_id}/')
    
    return redirect(f'/explore_topics/{user.username}/{readlist_id}/')


@login_required
def remove_paper_from_readlist(request, username):
    if request.method == 'POST':
        user = request.user
        paper_id = request.POST.get('paper_id')
        readlist_id = request.POST.get('readlist_id')
        readlist = get_object_or_404(Readlist, id=readlist_id, created_by=user)
        paper = get_object_or_404(ResearchPaper, id=paper_id)
        if paper in readlist.papers.all():
            readlist.papers.remove(paper)
            messages.success(request, f"{paper.title} has been removed from the readlist.")
        else:
            messages.error(request, "This paper is not in the readlist.")
        
        return redirect(f'/explore_topics/{user.username}/{readlist_id}/')

    return redirect(f'/explore_topics/{username}/')


def delete_readlist(request, username, id):
    logger.info("Request method is POST.")
    user = User.objects.get(username=username)
    try:
        readlist = get_object_or_404(Readlist, id=id, created_by=user)
        readlist.delete()
        messages.success(request, "Readlist deleted successfully.")
        return redirect(f'/explore_topics/{user.username}/')
    except Http404:
        logger.error("Readlist not found or does not belong to user.")
        messages.error(request, "Readlist not found.")
    except Exception as e:
        messages.error(request, "An error occurred while deleting the readlist.")

    return redirect(f'/explore_topics/{user.username}/')



def bytes_to_vector(vector_bytes):
    byte_io = io.BytesIO(vector_bytes)
    return np.load(byte_io)
def vector_to_bytes(vector):
    byte_io = io.BytesIO()
    np.save(byte_io, vector)
    byte_io.seek(0)
    return byte_io.read()



# nltk.download('punkt_tab') UNCOMMENT THESE LINE WHEN RUNNING THE SEARCH ENGINE FOR FIRST TIME
model = SentenceTransformer('all-MiniLM-L6-v2')
@login_required
def search_engine(request):
    if request.user:
        user = request.user 
        query = request.GET.get('query')

        vectors = []
        documents = []
        papers = ResearchPaper.objects.filter(user=user)

        for paper in papers:
            combined_text = None  # Initialize combined_text

            if VectorDocument.objects.filter(paper=paper).exists():
                vd = VectorDocument.objects.get(paper=paper)
                # Convert bytes back to vector
                vector = bytes_to_vector(vd.vector_representation)
                combined_text = vd.document  # Get the combined text from the existing VectorDocument
            else:
                combined_text = f"{paper.title} {paper.authors} {paper.extracted_text}".lower()
                vector = model.encode(combined_text)
                vector_bytes = vector_to_bytes(vector)  # Convert vector to bytes
                VectorDocument.objects.create(paper=paper, vector_representation=vector_bytes, document=combined_text)

            vectors.append(vector)
            documents.append(combined_text)  # This line is now safe

        vectors = np.array(vectors)
        qvector = model.encode(query)
        expanded_terms = expand_query(query)
        expanded_vectors = [model.encode(term) for term in expanded_terms]
        if expanded_vectors:
            combined_vector = np.mean([qvector] + expanded_vectors, axis=0)
        else:
            combined_vector = qvector

        # Using Hybrid approach (BM25 + cosine similarity) for calculating rankings
        bm25 = BM25Okapi([doc.split(" ") for doc in documents])
        query_tokens = query.split(" ")
        bm25_scores = bm25.get_scores(query_tokens)

        cosine_scores = cosine_similarity([combined_vector], vectors)[0]

        # Combine Scores
        combined_scores = 0.5 * bm25_scores + 0.5 * cosine_scores

        ranked_indices = np.argsort(combined_scores)[::-1]
        ranked_papers = [papers[int(i)] for i in ranked_indices]
        
        paginator = Paginator(ranked_papers, 10)
        page_number = request.GET.get('page')
        paginated_papers = paginator.get_page(page_number)

        return render(request, 'home/search_papers.html', {'ranked_papers': paginated_papers})



def expand_query(query):
    expanded_terms = set()
    expanded_terms.add(query)
    #adding synonyms
    synonyms = get_synonyms(query)
    expanded_terms.update(synonyms)
    #add contextual terms
    contextual_terms = get_contextual_terms(query)
    expanded_terms.update(contextual_terms)
    #add phrases
    phrases = get_phrases(query)
    expanded_terms.update(phrases)
    
    return list(expanded_terms)


def view_chroma_data(request):
    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(
        path=os.path.join(settings.BASE_DIR, 'chromadb_storage'),
        settings=Settings(),
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE,
    )
    
    # Get all collection names
    try:
        collections = chroma_client.list_collections()
        collection_names = [collection['name'] for collection in collections]

        # Get a specific collection
        collection_name = "research_papers"
        collection = chroma_client.get_collection(name=collection_name)

        # Retrieve all documents and embeddings from the collection
        research_papers = collection.get()  # Fetch all research papers
        combined_data = []

        # Check each paper for existing embeddings
        for paper_id in research_papers['ids']:
            existing_embeddings = collection.get(ids=[paper_id])
            combined_data.append({
                'id': paper_id,
                'document': existing_embeddings.get('documents', [])[0] if existing_embeddings.get('documents') else None,
                'embedding': existing_embeddings.get('embeddings', [])[0] if existing_embeddings.get('embeddings') else None,
            })

    except Exception as e:
        # Handle case where collection is not found or other errors
        combined_data = []
        collection_names = []
        print(f"Error fetching collections or data: {str(e)}")

    # Pass data to template
    context = {
        'combined_data': combined_data,
        'collection_names': collection_names,
    }

    return render(request, 'home/chroma_data.html', context)
