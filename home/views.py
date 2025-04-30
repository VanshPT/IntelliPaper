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
from .models import ResearchPaper, Folder, Readlist, Notes, VectorDocument, Citation, Chat, UserSession
from langchain_community.document_loaders import PyPDFLoader
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
from .helper import get_synonyms,get_contextual_terms, get_phrases, generate_citations, fetch_research_papers, refine_query, get_or_create_session,get_session_history
import nltk
from django.core.paginator import Paginator
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings,GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
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
            "max_output_tokens": 6000,
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
        Please generate a well-structured summary of the research article, using a mix of concise paragraphs and bullet points where appropriate. Organize the content in a visually appealing, engaging style that provides clarity for both technical and non-technical readers. If any specialized or technical terms are used that may be unfamiliar to a general audience, briefly explain each term immediately after it appears in the summary.
        """

        # Send the final summary request with retry logic
        final_summary_response = send_with_retry(summary_prompt)

        # Extract the main summary text from the response using regex (optional clean-up)
        raw_summary = final_summary_response.text

        # Send the cleaned summary as the response to the AJAX request
        return JsonResponse({"summary": raw_summary}, status=200)

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
        'email': user.email,
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
    You are tasked with clustering a collection of research papers submitted by users on our research assistant platform. Each entry in the collection consists of an ID, a title, and a portion of the abstract (the first part is the ID, followed by the title and a snippet of the abstract). Your job is to group these papers into meaningful clusters based on their topics.  

The goal is to create a user-friendly experience by generating clusters that serve both broad and specific research needs:  

1. **Broad-Level Clusters**: Include general categories like "Machine Learning," "Artificial Intelligence," "Blockchain," etc., where papers related to these overarching themes are grouped together.  

2. **Project-Specific Clusters**: Create focused clusters that align with specific topics or projects. For example, if multiple papers discuss "Fire Detection using Machine Learning," there should be a cluster named "Fire Detection" containing all related papers. These clusters should help users easily organize papers relevant to specific research projects or subtopics.  

Ensure the following:  
- A single paper can belong to multiple clusters if it is relevant to different topics.  
- Minimize the number of clusters while still maintaining clarity and relevance.  
- Always prioritize creating clusters that will provide the best user experience, helping users easily locate papers related to their research interests or projects.  

The output should strictly follow this format:  
cluster_name_1: [id1, id3]  
cluster_name_2: [id2, id5]  

Use only the IDs (the numbers at the start of each entry) in the output clusters. Do not include titles, abstracts, or explanations. Ensure the clusters are meaningful, concise, and aligned with the needs of real-world research use cases.  

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





model = SentenceTransformer('all-MiniLM-L6-v2')
@login_required
def search_engine(request):
    # nltk.download('wordnet') #UNCOMMENT THESE LINE WHEN RUNNING THE SEARCH ENGINE FOR FIRST TIME
    # nltk.download('punkt_tab') #UNCOMMENT THESE LINE WHEN RUNNING THE SEARCH ENGINE FOR FIRST TIME
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


embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=settings.GEMINI_API_KEY)

chroma_client = chromadb.PersistentClient(
    path=os.path.join(settings.BASE_DIR, 'chromadb_storage'),
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)



def get_context(refined_query, n):
    query_embedding = embedding_model.embed_query(refined_query)
    collection = chroma_client.get_or_create_collection(name="research_papers")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n
    )

    # Chroma returns documents as a list of lists (one per query embedding)
    raw_docs = results.get("documents", [])
    if raw_docs and isinstance(raw_docs[0], list):
        text_chunks = raw_docs[0]
    else:
        text_chunks = raw_docs

    # Print in copy-paste-ready form with triple-quotes:
    print("retrieval_context=[")
    for chunk in text_chunks:
        # Escape any """ inside the chunk to avoid breaking the string literal
        safe = chunk.replace('"""', '\\"\\"\\"')
        print(f'    """{safe}""",')
    print("]")

    return text_chunks



@login_required
def load_chats(request):
    print("load_chats view called")  # Debugging
    if request.method == 'POST':
        try:
            print('check1')
            user = User.objects.get(username=request.user)
            chats = Chat.objects.filter(session__user=user).order_by('timestamp')
            chat_list = [
                {"question": chat.question, "answer": chat.answer}
                for chat in chats
            ]
            print(f"Chat List: {chat_list}")  # Debugging
            return JsonResponse({"chats": chat_list})  # Ensure JsonResponse is used
        except Exception as e:
            print(f"Error in load_chats: {str(e)}")  # Debugging
            return JsonResponse({"error": str(e)}, status=500)
    else:
        print("Invalid request method in load_chats")  # Debugging
        return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def delete_chats(request):
    print('delete chats view activated')
    if request.method == 'POST':
        try:
            # Get the current user
            user = request.user
            
            # Find all UserSession objects for the user
            user_sessions = UserSession.objects.filter(user=user)
            
            # Delete all chats associated with the user's sessions
            deleted_count = 0
            for session in user_sessions:
                # Delete all Chat objects for this session
                count, _ = session.chats.all().delete()
                deleted_count += count
            
            # Log the deletion
            print(f"Deleted {deleted_count} chats for user: {user.username}")
            
            # Return success response
            return JsonResponse({
                "success": True,
                "message": f"Deleted {deleted_count} chat(s)."
            })
        except Exception as e:
            # Log the error
            print(f"Error deleting chats for user {user.username}: {str(e)}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)
    else:
        # Handle invalid request methods
        return JsonResponse({
            "success": False,
            "error": "Invalid request method. Use POST."
        }, status=405)
    


genai.configure(api_key=settings.GEMINI_API_KEY)
@login_required
def rag_assistant(request, username):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query')
            print(query)
            if not query:
                return JsonResponse({"error": "Query is required"}, status=400)
            
            # Retrieve session info and refine query based on conversation history.
            session_id = get_or_create_session(username)
            session=UserSession.objects.get(session_id=session_id)
            refined_query = refine_query(session_id, query)
            history= get_session_history(session_id)
            context = get_context(refined_query, 8)
            print(context)
            # Build the LangChain prompt template with detailed instructions.
            prompt_template = PromptTemplate(
                input_variables=["chat_history", "context", "user_query"],
                template="""
### Conversation History:
{chat_history}

### Context (Relevant excerpts from research articles):
{context}

### User Query:
{user_query}

### Instructions:(these are system instructions, dont reply or react to them just follow them. answer only to {user_query})
1. First, review the conversation history to understand the background.
2. If the user query is a generic statement (e.g., "ok", "thank you", "alright") that doesn't require context, respond in a friendly and generic manner without relying on the provided context.
3. If the user is asking a question and the answer is present in the context, extract and use the relevant information.
4.
    When encountering technical or scientific terms in the context that may be unfamiliar to a general audience, provide a brief explanation in parentheses immediately after the term. This includes terms that are specific to certain communities or fields (e.g., "Fine Tuning" in the context of AI). Ensure that the explanation is concise, clear, and accessible to someone without a specialized background.

    Examples:

    If the term "Fine Tuning" appears, explain it as: "Fine Tuning (a process in AI where a pre-trained model is further trained on a specific dataset to improve its performance on a particular task)."

    If the term "Neural Network" appears, explain it as: "Neural Network (a system of algorithms designed to recognize patterns, modeled loosely after the human brain)."

    Goal:
    Make the response inclusive and understandable for readers from diverse backgrounds, ensuring that no technical term is left unexplained.
5. Use bullet points if summarizing multiple points.
6. Keep the answer concise, clear, and accessible for someone without an academic background.
7. Always consider the conversation history first, then the context.
8. if user asks your name, respond I am your research assistant. I will answer your queries related to your research articles in an easy and engaging manner. Dont repeat exact same sentence make up your own sentence for this while generating.
9. Keep answers in depth and explanatory, dont shy away from giving long answers.
    
Provide only the final answer.
"""
            )
            
            
            # Create the Gemini LLM instance using LangChain's GoogleGenerativeAI wrapper.
            gemini_llm = GoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=1,
                top_p=0.95,
                top_k=50,
                max_output_tokens=500000,
                google_api_key=settings.GEMINI_API_KEY
            )
            
            # Create the LLMChain with the prompt template and the Gemini LLM.
            chain = LLMChain(llm=gemini_llm, prompt=prompt_template)
            # Execute the chain using conversation history, context, and the refined user query.
            final_response = chain.run(
                chat_history=history,
                context=context,
                user_query=query
            )
            Chat.objects.create(
                session=session,
                question=query,
                answer=final_response
            )
            return JsonResponse({"message": final_response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)






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

