from nltk.corpus import wordnet
import nltk
import logging
from nltk import ngrams
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.pdf import PyPDFLoader

import requests
from bs4 import BeautifulSoup
import time

# nltk.download('wordnet') #UNCOMMENT THESE LINE WHEN RUNNING THE SEARCH ENGINE FOR FIRST TIME
# nltk.download('punkt_tab') #UNCOMMENT THESE LINE WHEN RUNNING THE SEARCH ENGINE FOR FIRST TIME
def get_synonyms(query):
    synonyms = set()
    for syn in wordnet.synsets(query):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)



nlp = spacy.load("en_core_web_md")
def get_contextual_terms(query, top_n=5):
    query_doc = nlp(query)
    query_vector = query_doc.vector.reshape(1, -1)
    words = list(nlp.vocab.strings)
    word_vectors = np.array([nlp.vocab[word].vector for word in words if nlp.vocab[word].has_vector])
    similarities = cosine_similarity(query_vector, word_vectors)
    similar_indices = np.argsort(similarities[0])[-top_n:]
    contextual_terms = [words[i] for i in similar_indices]

    return contextual_terms

def get_phrases(query):
    tokens = nltk.word_tokenize(query)
    n_gram_phrases = ngrams(tokens, 2)
    phrases = [' '.join(gram) for gram in n_gram_phrases]
    doc = nlp(query)
    named_entities = [ent.text for ent in doc.ents]
    return list(set(phrases + named_entities))


def generate_citations(paper):
    pdf_path = paper.pdf_file.path
    pdf_loader = PyPDFLoader(pdf_path)
    document = pdf_loader.load()

    # Extract only the first and last three pages
    num_pages = len(document)
    relevant_pages = []

    # Add first three pages
    relevant_pages.extend(document[:5])  # Take the first three pages

    # Add last three pages, ensuring not to exceed total pages
    if num_pages > 3:
        relevant_pages.extend(document[-5:])  # Take the last three pages

    # Join page contents into full text
    full_text = "\n".join([page.page_content for page in relevant_pages])

    # Configure Gemini API key
    genai.configure(api_key=settings.GEMINI_API_KEY)

    # Define generation configuration
    generation_config = {
        "temperature": 0.0,  # More deterministic responses
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 400,  # Adjust this based on expected response size
        "response_mime_type": "text/plain",
    }

    # Initialize the Gemini model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Start a new chat session
    chat_session = model.start_chat(history=[])

    # Split the full text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1300, chunk_overlap=200)
    text_chunks = text_splitter.split_text(full_text)

    # Prepare to send each chunk to the Gemini API
    prompt_template = """
    Based on the following excerpts from a research paper, please consider the context of **all chunks** provided and generate citations in multiple specified formats. Ensure that you **wait until all chunks have been processed** before generating the final citations.
    Excerpt:
    {chunk}
    Once all chunks have been processed, provide the citations using the following formats:
    **APA Citation**:
    <p>...</p>

    **MLA Citation**:
    <p>...</p>

    **Chicago Citation**:
    <p>...</p>

    **Harvard Citation**:
    <p>...</p>

    Make sure to find all citation types from the excerpts provided and respond with the following structure:
        - The **name** of the citation format in bold.
        - The actual citation in the respective format after the name.
    Please ensure the output includes all relevant citations you found after processing the chunks.
    """

    # Counter for API calls
    api_call_count = 0

    # Iterate through each chunk and process
    for i, chunk in enumerate(text_chunks):
        if chunk.strip():  # Check if the chunk is not empty
            prompt = prompt_template.format(chunk=chunk)
            try:
                # Send the prompt to Gemini and get the response
                response = chat_session.send_message(prompt)
                api_call_count += 1

                # Log the response for debugging
                logging.info(f"Processed chunk {i + 1}/{len(text_chunks)}: {response.text.strip()}")

                # Sleep after every 5 API calls
                if api_call_count % 5 == 0:
                    time.sleep(2)  # Sleep for 2 seconds

                # Check if the response contains an error message
                if "<p>Error generating final citations</p>" in response.text:
                    logging.warning("Discarding response due to error message.")
                    return None  # Discard and stop processing if error message is found

            except Exception as e:
                logging.error(f"Error during LLM processing with Gemini for chunk {i + 1}: {e}")

    # After processing all chunks, request the final citations
    final_prompt = """
    Based on all the previously processed excerpts, please provide the citations in the following format:
    <>APA Citation: ...</p>
    <p>MLA Citation: ...</p>
    <p>Chicago Citation: ...</p>
    <p>Harvard Citation: ...</p>
    """

    try:
        # Send the final prompt to get the citations
        final_response = chat_session.send_message(final_prompt)
        citations = final_response.text.strip()

        # Check if the final response contains an error message
        if "<p>Error generating final citations</p>" in citations:
            logging.warning("Final citations response contained an error message. Discarding.")
            return None  # Discard final citations if error message is found
    except Exception as e:
        logging.error(f"Error during final LLM processing with Gemini: {e}")
        return None  # Return None if there's an error

    return citations
    


# Function to fetch and parse research papers
def fetch_research_papers(query, max_pages=3):
    base_url = f"https://arxiv.org/search/?query={query}&searchtype=all&abstracts=show&size=50&order=-announced_date_first"
    papers = []

    # Set headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Loop through the pages
    for page in range(max_pages):
        print(f"Scraping page {page + 1}")
        url = f"{base_url}&start={page * 50}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            continue

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        entries = soup.find_all("li", class_="arxiv-result")

        # Extract details from each entry
        for entry in entries:
            try:
                title = entry.find("p", class_="title").text.strip()
                authors = entry.find("p", class_="authors").text.strip()
                abstract = entry.find("p", class_="abstract-full").text.strip()  # Changed to abstract-full
                link = entry.find("p", class_="list-title").find("a")["href"]

                papers.append({
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "link": f"https://arxiv.org{link}"
                })
            except AttributeError:
                continue

        # Add delay to avoid overwhelming the server
        time.sleep(2)

    # Return the results as a nested JSON-like structure
    return {"papers": papers}

# Example usage (you can call this function from your Django views)
# papers_data = fetch_research_papers(query="machine learning", max_pages=3)
# print(papers_data)
