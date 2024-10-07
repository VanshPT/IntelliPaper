import os
import logging
from django_q.tasks import async_task
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama
import chromadb
from .models import ResearchPaper
from django.conf import settings
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(
    path=os.path.join(settings.BASE_DIR, 'chromadb_storage'),
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

# Set up logger for error handling
logger = logging.getLogger(__name__)

def load_documents():
    """Asynchronously process all research papers and update ChromaDB with vector embeddings."""
    try:
        # Fetch all research papers
        research_papers = ResearchPaper.objects.all()
        
        # Access the collection in ChromaDB
        collection = chroma_client.get_or_create_collection(name="research_papers")
        
        for paper in research_papers:
            # Check if embeddings for this paper already exist in the collection
            existing_embeddings = collection.get(ids=[str(paper.id)])

            if existing_embeddings["ids"]:
                print(f"Paper ID {paper.id} already has embeddings in ChromaDB.")
                continue  # Skip if embeddings exist

            # Load the PDF for the paper
            pdf_path = paper.pdf_file.path
            if not os.path.exists(pdf_path):
                logger.error(f"PDF not found for paper ID {paper.id}: {pdf_path}")
                continue  # Skip if PDF file does not exist

            print(f"Processing paper ID {paper.id}, PDF path: {pdf_path}")
            pdf_loader = PyPDFDirectoryLoader(os.path.dirname(pdf_path))
            document = pdf_loader.load()

            # Extract the full text from the PDF
            full_text = "\n".join([page.page_content for page in document])
            print(f"Extracted text for paper ID {paper.id}: {full_text[:200]}...")  # Log first 200 characters

            # Split the text into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            text_chunks = text_splitter.split_text(full_text)
            print(f"Created {len(text_chunks)} chunks for paper ID {paper.id}")

            # Embed each chunk using Ollama embeddings (using mxbai-embed-large model)
            all_embeddings = []
            for chunk in text_chunks:
                response = ollama.embeddings(model="nomic-embed-text", prompt=chunk)
                embedding = response["embedding"]
                all_embeddings.append(embedding)

            # Combine all chunk embeddings into a single embedding for the full document
            document_embedding = [sum(x) for x in zip(*all_embeddings)]
            print(f"Generated combined embeddings for paper ID {paper.id}")
            print(f"{paper.id}-{document_embedding}")

            # Store embeddings in ChromaDB with the paper ID as the key
            collection.add(
                ids=[str(paper.id)],
                embeddings=[document_embedding],
                documents=[full_text]
            )
            print(f"Stored embeddings for paper ID {paper.id} in ChromaDB")

    except Exception as e:
        logger.error(f"Error processing papers: {str(e)}")
