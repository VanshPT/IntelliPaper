from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
import os
import io
import re
import json
from django.conf import settings
from django.urls import reverse
from .models import ResearchPaper, Folder, Readlist, Notes, VectorDocument, Citation
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from django.contrib import messages
import google.generativeai as genai
import logging
from sentence_transformers import SentenceTransformer
import numpy as np
from django.contrib.auth.models import User
from sklearn.metrics.pairwise import cosine_similarity
import time
import requests
from rank_bm25 import BM25Okapi
from .helper import get_synonyms,get_contextual_terms, get_phrases, generate_citations, fetch_research_papers
import nltk
from django.core.paginator import Paginator
from langchain.embeddings import HuggingFaceEmbeddings
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
# from langchain_community.llms import Ollama
#below are imports for running async tasks
from django_q.tasks import async_task



# Set up logging for errors
logger = logging.getLogger(__name__)

# Landing view
def landing(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
    return render(request, 'home/landing/landing.html', context)


@login_required
def render_dashboard(request, username):
    user = request.user
    latest_papers = ResearchPaper.objects.filter(user=user).order_by('-upload_datetime')[:8]
    async_task('home.tasks.process_pdf_documents')
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
    user_instance = User.objects.get(username=user)

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
def extract_save_pdf(request):
    if request.method == "POST" and request.FILES.get('pdf_file'):
        user = request.user
        pdf_file = request.FILES['pdf_file']
        file_path = default_storage.save(f"data/{pdf_file.name}", pdf_file)
        perm_file_path = default_storage.save(f"pdfs/{pdf_file.name}", pdf_file)
        absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        async_task(process_pdf, user.username, absolute_file_path, pdf_file.name)
        messages.success(request, "Your paper is being processed and will be uploaded soon.")
        return redirect(f"/dashboard/{user.username}")
    return render(request, 'upload_pdf.html')


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
    if request.user.username != username:
        messages.error(request, "You are not logged in with this username")
        return redirect('/')
    
    papers = ResearchPaper.objects.filter(user=request.user)
    if papers.count() == 0:
        messages.info(request, "No PDFs exist in your account.")
        return redirect(f'/auto_cluster/{username}')
    if papers.count() == 1:
        messages.info(request, "Only one paper exists in your account.")
        return redirect(f'/auto_cluster/{username}')

    # Prepare custom documents in the format {id}-{title}-{abstract}
    paper_docs = prepare_custom_documents(papers)
    
    # Send the paper docs to Gemini for intelligent clustering and naming
    cluster_mapping = intelligent_clustering_via_gemini(paper_docs)
    
    # Save the clusters with the new names
    save_clusters_gemini_based(cluster_mapping, request.user)
    
    return redirect(f'/auto_cluster/{request.user.username}')


def prepare_custom_documents(papers):
    """
    Prepare documents for each paper in the format {id}-{title}-{abstract}.
    """
    paper_docs = []
    for paper in papers:
        custom_doc = f"{paper.id}-{paper.title}-{paper.abstract[:500]}"
        paper_docs.append(custom_doc)
    return paper_docs


def intelligent_clustering_via_gemini(paper_docs):
    """
    Send the custom documents to Gemini for clustering and get cluster names and labels.
    """
    # Configure Gemini API key
    genai.configure(api_key=settings.GEMINI_API_KEY)

    # Define generation configuration
    generation_config = {
        "temperature": 0.0,  # More deterministic responses
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 300,  # Limit tokens to avoid resource issues
        "response_mime_type": "text/plain",
    }

    # Initialize the Gemini model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Start a new chat session (reuse this for all requests)
    chat_session = model.start_chat(history=[])

    # Create the prompt for Gemini API
    prompt_template = """
    You are given a list of research papers where each entry consists of an ID, a title, and an abstract (the first part is the ID, followed by the title and a portion of the abstract). Your task is to cluster these papers based on their topics.

The output should strictly follow this format:
cluster_name_1: [id1, id3]
cluster_name_2: [id2, id5]

Please make sure you only use the IDs (the numbers at the start of each entry) in the output clusters. Do not include titles or explanations, just return the cluster names and the list of corresponding IDs in the format shown above. Also note one paper can be clustered into multiple folders also. let me give you an example you should cluster like that. lets say we got three papers based on fire detecton system project usign ml or dl or lany other techniques, so one cluster should definitely be named fire detection system which should have all these ids of papers related to this topic, also they can be part of another paper, in short best experience should be provided to a real life user use case, if i am making a good project on some topic and researching multiple aproaches, one folder should compulsarily be found there containing all the papers uploaded regarding that project topic. so clusters with such project based like clustering should also be there and also clusters which little broad range of clustering both types of clusters. Best User experience should always be provided, if i am researching on some project topic you have to intelligently give a cluster based on this topic. Also numbers of clusters generated should be minimal only important ones while still giving proper clusters.

Here are the documents:
{paper_docs}
    """

    # Create the prompt with paper documents
    prompt = prompt_template.format(paper_docs="; ".join(paper_docs))

    try:
        # Send the prompt to Gemini and get the response
        response = chat_session.send_message(prompt)
        print("raw: ",response.text)
        cluster_mapping = parse_gemini_response(response.text)

    except Exception as e:
        logging.error(f"Error during clustering with Gemini: {e}")
        raise

    return cluster_mapping


def parse_gemini_response(response_text):
    """
    Parse the response from Gemini to extract cluster mappings.
    We expect the format: Cluster Name: [id1, id2, id3]
    """
    cluster_mapping = {}

    try:
        # Match each line that contains a cluster name and its associated paper IDs
        clusters = re.findall(r"([A-Za-z0-9\s\-&,]+): \[(.*?)\]", response_text)

        for cluster_name, paper_ids_str in clusters:
            # Convert the paper IDs string into a list of integers
            paper_ids = [int(paper_id.strip()) for paper_id in paper_ids_str.split(',')]
            cluster_mapping[cluster_name.strip()] = paper_ids
    except Exception as e:
        logging.error(f"Error parsing Gemini response: {e}")

    return cluster_mapping


def save_clusters_gemini_based(cluster_mapping, user):
    """
    Save the clusters generated by Gemini with appropriate names.
    """
    # Delete all existing folders for this user before creating new clusters
    Folder.objects.filter(created_by=user).delete()

    for cluster_name, paper_ids in cluster_mapping.items():
        print(f"Saving cluster: {cluster_name} with papers: {paper_ids}")
        # Create a new folder for each cluster
        folder = Folder.objects.create(name=cluster_name, created_by=user)
        
        # Fetch ResearchPaper objects using the IDs and associate them with the folder
        papers = ResearchPaper.objects.filter(id__in=paper_ids)
        folder.papers.set(papers)
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


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
chroma_client = chromadb.PersistentClient(
    path=os.path.join(settings.BASE_DIR, 'chromadb_storage'),
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

@login_required
def rag_assistant(request, username):
    if request.method == 'POST':
        try:
            # Get the JSON body from the request
            data = json.loads(request.body)
            query = data.get('query')

            if not query:
                return JsonResponse({"error": "No query provided"}, status=400)


            # Convert the query to vector using the same embeddings model
            query_embedding = embedding_model.embed_query(query)
            # Access the research_papers collection in ChromaDB
            collection = chroma_client.get_or_create_collection(name="research_papers")

            # Query the top 3 results from ChromaDB
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=3
            )

            # print(f"Top 3 results retrieved from ChromaDB: {results}")

            # Extract paper IDs and corresponding excerpts
            paper_ids = [chunk_id.split('_')[0] for chunk_id in results['ids'][0]]
            excerpts = [result for result in results['documents'][0]]

            # Fetch titles of papers from the ResearchPaper model
            papers = ResearchPaper.objects.filter(id__in=paper_ids)
            paper_titles = {str(p.id): p.title for p in papers}

            # Create excerpts for the prompt
            paper_excerpts = " ".join(excerpts)

            # Prepare the prompt for the Gemini API
            prompt = f"""
            Answer taking full below prompt in mind as a whole.
            This is Users Query: {query},  Also check once if text excerpts provided satisfy the user query or not, if yes then generate normally and ignore this line, if the query is any general question like "Hii, how are you" or anything which doesnt relate to excerpts even slightly then only take query into consideration and answer accordingly, dont even mention excerpts or query just answer directly from query and ignore the rest of prompt. If someone asks you who are you , your name is Intellipaper Research Assistant.
            Based on the following paper excerpts, provide a meaningful answer to the user's query. 
            Please quote crucial sentences and show the titles of the papers from which the answers are extracted.
            If no results obtained, give output from your own answer and show no excerpts found.
            Text excerpts: 
            {paper_excerpts}
            """

            # Configure Gemini API key
            genai.configure(api_key=settings.GEMINI_API_KEY)

            # Define generation configuration
            generation_config = {
                "temperature": 0.0,  # More deterministic responses
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 200,  # Increase the token limit if needed
                "response_mime_type": "text/plain",
            }

            # Initialize the Gemini model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
            )

            # Start a new chat session
            chat_session = model.start_chat(history=[])

            # Send the prompt to Gemini and get the response
            response = chat_session.send_message(prompt)
            answer = response.text.strip()

            # Format the output to include the paper titles
            formatted_response = f"{answer}\n\nSources:\n"
            added_titles = []  # List to keep track of added paper titles
            for paper_id in paper_ids:
                if paper_id in paper_titles:
                    title = paper_titles[paper_id]
                    if title not in added_titles:  # Check if the title is already added
                        formatted_response += f"- {title}\n"
                        added_titles.append(title)

            return JsonResponse({"message": formatted_response}, status=200)

        except Exception as e:
            print(f"Error in RAG Assistant: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

class GenerateCitationsView(View):
    def get(self, request, paper_id):
        paper = ResearchPaper.objects.get(id=paper_id)
        
        citations = Citation.objects.filter(paper=paper).first()
        if citations:
            return JsonResponse({'citations': citations.citations, 'existing': True})
        generated_citations = generate_citations(paper)

        citations = Citation.objects.create(
            user=request.user,
            paper=paper,
            citations=generated_citations
        )
        
        return JsonResponse({'citations': citations.citations, 'existing': False})


 
@login_required
def web_search(request):
    query = request.GET.get('query')
    results = fetch_research_papers(query)
    paper_list = results['papers']

    # Set up pagination with 10 items per page
    paginator = Paginator(paper_list, 12)
    page_number = request.GET.get('page', 1)
    ranked_papers = paginator.get_page(page_number)

    context = {
        'results': ranked_papers,
        'query': query,
    }
    return render(request, 'home/search_web_papers.html', context)