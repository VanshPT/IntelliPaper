import os
import logging
from django_q.tasks import async_task
import chromadb
from .models import ResearchPaper
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from django.conf import settings
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from .views import prepare_custom_documents, intelligent_clustering_via_gemini, save_clusters_gemini_based
from django.contrib.auth.models import User

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(
    path=os.path.join(settings.BASE_DIR, 'chromadb_storage'),
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

# Set up logger for error handling
logger = logging.getLogger(__name__)

# Initialize HuggingFace embeddings model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def process_pdf_documents():
    """Check if all papers have vectors stored for all their blocks in ChromaDB, and update as necessary."""
    try:
        # Fetch all research papers
        research_papers = ResearchPaper.objects.all()
        print(f"Total research papers to process: {len(research_papers)}")
        
        # Access or create the collection in ChromaDB
        collection = chroma_client.get_or_create_collection(name="research_papers")
        print(f"ChromaDB collection accessed or created successfully.")
        for paper in research_papers:
            # Load the PDF for the paper
            pdf_path = paper.pdf_file.path
            if not os.path.exists(pdf_path):
                logger.error(f"PDF not found for paper ID {paper.id}: {pdf_path}")
                # print(f"PDF not found for paper ID {paper.id}")
                continue  # Skip if PDF file does not exist

            print(f"Processing paper ID {paper.id}, PDF path: {pdf_path}")
            pdf_loader = PyPDFLoader(pdf_path)
            document = pdf_loader.load()

            # Extract the full text from the PDF
            full_text = "\n".join([page.page_content for page in document])
            print(f"Extracted text for paper ID {paper.id}: {full_text[:200]}...")

            # Split the text into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            text_chunks = text_splitter.split_text(full_text)
            print(f"Created {len(text_chunks)} chunks for paper ID {paper.id}")

            # Process each chunk
            for chunk_index, chunk in enumerate(text_chunks):
                # Generate a unique ID for each chunk
                chunk_id = f"{paper.id}_{chunk_index+1}"
                print(f"Processing chunk {chunk_index+1}/{len(text_chunks)} for paper ID {paper.id}")

                # Check if embeddings for this chunk already exist in ChromaDB
                existing_embeddings = collection.get(ids=[chunk_id])
                if existing_embeddings["ids"]:
                    print(f"Chunk ID {chunk_id} already has embeddings in ChromaDB. Skipping...")
                    continue  # Skip if embeddings exist

                # Embed the chunk using HuggingFace embeddings
                embedding = embedding_model.embed_documents([chunk])[0]
                print(f"Generated embedding for chunk {chunk_index+1} of paper ID {paper.id}")

                # Store chunk embeddings in ChromaDB with the chunk ID
                collection.add(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    documents=[chunk]
                )
                print(f"Stored embeddings for chunk ID {chunk_id} in ChromaDB")

    except Exception as e:
        logger.error(f"Error processing papers: {str(e)}")
        print(f"Error processing papers: {str(e)}")

def auto_cluster_task(user_id):
    try:
        # Fetch user instance
        user = User.objects.get(id=user_id)
        
        # Fetch papers associated with the user
        papers = ResearchPaper.objects.filter(user=user)
        if papers.count() < 2:
            # Exit if no clustering can be done due to insufficient papers
            return "Insufficient papers for clustering"

        # Prepare custom documents for clustering
        paper_docs = prepare_custom_documents(papers)
        
        # Perform clustering using Gemini
        cluster_mapping = intelligent_clustering_via_gemini(paper_docs)
        
        # Save the cluster results
        save_clusters_gemini_based(cluster_mapping, user)
        
        return "Clustering completed successfully"
    except User.DoesNotExist:
        return "User not found"