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
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings,GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import requests
from bs4 import BeautifulSoup
import time
import json
import uuid
from .models import UserSession,Chat
from django.contrib.auth.models import User

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


def get_or_create_session(username):
    user=User.objects.get(username=username)
    session_obj, created = UserSession.objects.get_or_create(
        user=user,
        defaults={"session_id": str(uuid.uuid4())}  # Generate new session ID if not exists
    )
    return session_obj.session_id

def get_session_history(session_id):
    # Retrieve the user session based on the unique session_id
    user_session = UserSession.objects.get(session_id=session_id)
    
    # Use the related name 'chats' to get all Chat objects for the session, ordered by timestamp
    chats = user_session.chats.order_by("timestamp")
    
    # Format chat history as a list of message dictionaries expected by the Gemini API
    history = []
    for chat in chats:
        history.append({"role": "user", "text": chat.question})
        history.append({"role": "assistant", "text": chat.answer})
      
    if len(history) > 30:
        history = history[-15:]

    return history





def refine_query(session_id, query):
    # Retrieve the conversation history for the given session
    history_items = get_session_history(session_id)
    chat_history = "\n".join(
        f"{item.get('role', 'User').capitalize()}: {item.get('message', '')}"
        for item in history_items
    )
    print(chat_history)
    
    # Define the prompt template to instruct the LLM on refining the query
    prompt_template = PromptTemplate(
        input_variables=["chat_history", "user_query"],
        template="""
### Conversation History:
{chat_history}

### Raw User Query:
{user_query}

### Instructions:
1. Analyze the conversation history to understand the research context.
2. Identify if the user has referenced specific research articles, topics, or technical terms.
3. If the query is ambiguous or too terse, refine it by incorporating relevant keywords and context extracted from the history.
4. Ensure the refined query is concise, clear, and rich in information so that it retrieves the best matching document chunks from research articles.
5. Output only the refined query without any additional commentary.
6. If query is general statement and you feel it doesnt need refinement, then give that query as it is.

### Example:
**Chat History:**
- User: "Can you explain the findings of the paper on neural networks by Doe et al. 2023?"  
- AI: "The paper discusses improvements in convolutional neural networks using dropout techniques."

**Raw User Query:**
"Dropout effectiveness"

**Refined Query Output:**
"Effectiveness of dropout in enhancing convolutional neural networks as per Doe et al. 2023"
"""
    )

    # Configure the Gemini LLM for refining queries with a lower temperature for accuracy.
    genai_model = GoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3,
        top_p=0.9,
        top_k=30,
        max_output_tokens=100,
        google_api_key=settings.GEMINI_API_KEY
    )

    # Create an LLMChain with the prompt template and the Gemini model.
    chain = LLMChain(llm=genai_model, prompt=prompt_template)

    # Run the chain with the session's chat history and the raw user query.
    refined_query = chain.run(chat_history=chat_history, user_query=query)

    return refined_query.strip()