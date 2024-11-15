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
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
import time
import json

# nltk.download('wordnet') #UNCOMMENT THESE LINE WHEN RUNNING THE SEARCH ENGINE FOR FIRST TIME
# nltk.download('punkt_tab') #UNCOMMENT THESE LINE WHEN RUNNING THE SEARCH ENGINE FOR FIRST TIME

# 1. Synonym Expansion
def get_synonyms(query):
    synonyms = set()
    for syn in wordnet.synsets(query):
        for lemma in syn.lemmas():
            if lemma.name() != query:  # Avoid adding the original word
                synonyms.add(lemma.name().replace('_', ' '))  # Replace underscores with spaces
    return list(synonyms)

# 2. Contextual Expansion using Word Embeddings
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

# 3. Phrase Detection and Expansion
def get_phrases(query):
    tokens = nltk.word_tokenize(query)
    n_gram_phrases = ngrams(tokens, 2)
    phrases = [' '.join(gram) for gram in n_gram_phrases]
    doc = nlp(query)
    named_entities = [ent.text for ent in doc.ents]
    return list(set(phrases + named_entities))

# # 4. Query Rewriting with Relevance Feedback
# def relevance_feedback(query, feedback_terms):
#     # Combine original query with feedback terms
#     return query + " " + " ".join(feedback_terms)


# # 5. Spell Correction and Normalization
# def normalize_and_correct_spelling(query):
#     # Correct spelling using TextBlob and convert to lowercase for normalization
#     corrected_query = str(TextBlob(query).correct())
#     return corrected_query.lower()


# # 6. Removing Stop Words and Redundant Terms
# def remove_stopwords(query):
#     # Remove common stop words to reduce noise
#     stop_words = set(stopwords.words('english'))
#     return " ".join([word for word in query.split() if word.lower() not in stop_words])






def query_refiner(query):
    # Print the query to ensure it reaches this point
    print("Original Query:", query)

    # Configure the API key
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        print("Error configuring API key:", e)
        return "ERROR", "Failed to configure API key"

    # Initialize the model with generation configuration
    generation_config = {
        "temperature": 0.7,  # Balanced for determinism and variability
        "top_p": 0.9,       # Focused on high-probability tokens
        "top_k": 20,        # Limits options to the top-k most likely words
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",  # Expect JSON response
    }

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-8b",
            generation_config=generation_config,
        )
    except Exception as e:
        print("Error initializing the GenerativeModel:", e)
        return "ERROR", "Failed to initialize the GenerativeModel"

    # Define the prompt template for refining and classifying the query
    prompt_template = f"""
    You are an advanced assistant specializing in scientific and technical domains. Your task is to refine, rephrase, or expand a user query so it is more precise and aligned for retrieval of relevant scientific or technical information from a database.

    1. If the query is general knowledge or unrelated to scientific/technical topics, classify it as "GENERAL" and return the query unchanged.
    2. If the query is scientific/technical in nature:
       - Rewrite it to make the intent clear and specific.
       - Expand it if necessary to include additional terms or synonyms that may improve retrieval accuracy.
       - Add clarifying details if the query seems ambiguous or incomplete.
       - Avoid altering the core meaning or intent of the original query.

    Respond strictly in JSON format:
    {{
      "classification": "[GENERAL/SCIENTIFIC]",
      "refined_query": "[Your refined query here]"
    }}

    **Original Query**: "{query}"
    """

    # Start a chat session and send the message
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt_template)
        output_text = response.text  # Get the raw text response
        print("Raw Response:", output_text)  # Debug raw response

        # Parse the response as JSON
        output_json = json.loads(output_text)
    except Exception as e:
        print("Error during chat session or message send:", e)
        return "ERROR", "Failed to process the chat session"

    # Extract values from the JSON response
    try:
        classification = output_json.get("classification", "ERROR")
        refined_query = output_json.get("refined_query", "ERROR")
    except Exception as e:
        print("Error extracting values from JSON response:", e)
        return "ERROR", "Failed to extract values"

    # Print for debugging purposes
    print("Classification:", classification)
    print("Refined Query:", refined_query)

    # Return the classification and refined query
    return classification, refined_query

def generate_citations(paper):
    pdf_path = paper.pdf_file.path
    pdf_loader = PyPDFLoader(pdf_path)
    document = pdf_loader.load()

    # Extract only the first and last three pages
    num_pages = len(document)
    relevant_pages = document[:5] + document[-5:] if num_pages > 5 else document

    # Join page contents into full text
    full_text = "\n".join([page.page_content for page in relevant_pages])

    # Configure Gemini API key
    genai.configure(api_key=settings.GEMINI_API_KEY)

    # Define generation configuration
    generation_config = {
        "temperature": 0.0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 4000,
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

    # Updated prompt template for strict citation format adherence
    prompt_template = """
    From the following excerpt, identify or generate citations in APA, MLA, Chicago, and Harvard formats.
    Provide only the citations in the following structure, without any additional text or commentary:

    - **APA Citation**: <APA citation here>
    - **MLA Citation**: <MLA citation here>
    - **Chicago Citation**: <Chicago citation here>
    - **Harvard Citation**: <Harvard citation here>

    Excerpt:
    {chunk}
    """

    api_call_count = 0
    all_responses = []

    # Process each chunk individually
    for i, chunk in enumerate(text_chunks):
        if chunk.strip():
            prompt = prompt_template.format(chunk=chunk)
            try:
                response = chat_session.send_message(prompt)
                api_call_count += 1

                # Collect each response for further processing
                all_responses.append(response.text.strip())

                # Sleep after every 5 API calls to avoid rate limiting
                if api_call_count % 5 == 0:
                    time.sleep(2)

                # Check for specific error patterns
                if "Error generating" in response.text:
                    logging.warning(f"Error detected in response for chunk {i + 1}, skipping this chunk.")
                    continue

            except Exception as e:
                logging.error(f"Error processing chunk {i + 1}: {e}")

    # Final prompt to consolidate citations
    final_prompt = """
    Consolidate the following citations, ensuring all 4 formats (APA, MLA, Chicago, Harvard) are included.
    Provide only the citations in this exact structure, without any additional text or commentary:

    - **APA Citation**: <APA citation here>
    - **MLA Citation**: <MLA citation here>
    - **Chicago Citation**: <Chicago citation here>
    - **Harvard Citation**: <Harvard citation here>

    Previous responses:
    {all_responses}
    """

    # Format the responses to use in the final prompt
    all_responses_text = "\n\n".join(all_responses)
    final_prompt = final_prompt.format(all_responses=all_responses_text)

    try:
        final_response = chat_session.send_message(final_prompt)
        citations = final_response.text.strip()

        # Final validation to ensure no error messages are in the response
        if "Error generating" in citations:
            logging.warning("Final response contained an error message.")
            return None
    except Exception as e:
        logging.error(f"Error in final citation generation: {e}")
        return None

    return citations

# Function to fetch and parse research papers
def fetch_research_papers(query, max_pages=3):
    base_url = f"https://arxiv.org/search/?query={query}&searchtype=all&abstracts=show&size=50&order=-announced_date_first"
    papers = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for page in range(max_pages):
        url = f"{base_url}&start={page * 50}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        entries = soup.find_all("li", class_="arxiv-result")

        for entry in entries:
            try:
                title = entry.find("p", class_="title").text.strip()
                authors = entry.find("p", class_="authors").text.replace("Authors:", "").replace("\n", " ").strip()
                abstract = entry.find("p", class_="abstract").text.strip()
                link = entry.find("p", class_="list-title").find("a")["href"]

                papers.append({
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "link": link  # Link is already complete
                })
            except AttributeError:
                continue

    return {"papers": papers}

