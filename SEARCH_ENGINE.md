---

# 📖 Search Engine: Detailed Documentation and Implementation Guide

This document provides an in-depth explanation of how traditional Information Retrieval (IR) systems are constructed, the steps involved, and how we have implemented these steps in the **IntelliPaper** search engine. We will cover the techniques, tools, algorithms, and methodologies used, along with a discussion on their advantages and limitations.

---

## 1. Introduction to Information Retrieval (IR) Systems

An **Information Retrieval (IR)** system is a set of algorithms designed to retrieve information from a large repository of documents or data, relevant to a user’s query. The goal of an IR system is to return the most relevant documents efficiently and accurately.

At a high level, the process of building an IR system includes:
1. **Document Processing and Indexing**
2. **Query Processing and Vectorization**
3. **Query Expansion**
4. **Document Ranking and Retrieval**
5. **Evaluation and Optimization**

In our case, the repository comprises research papers, and the IR system helps users find papers relevant to their research needs.

---

## 2. Building Blocks of an IR System

### 2.1 Document Processing and Indexing

The first step in building an IR system is to process the collection of documents that will be searched. This involves:
- **Text extraction** from documents.
- **Metadata extraction** (such as title, author, abstract, etc.).
- **Vectorization** of the document content to make it searchable.

#### IntelliPaper's Implementation:
1. **Text Extraction:**
   - We extract the **title**, **author**, and the **first five pages of the paper** from each PDF. This is because research papers often contain most of their key terms within the first few pages (title, abstract, introduction).
   - We redundantly add the **title** and **author** fields during indexing to give them more weight in search results.
   
2. **Document Vectorization:**
   - We use **Sentence-BERT embeddings** to convert the extracted text into **context-aware vectors**. BERT embeddings provide a rich, contextual understanding of the text, capturing the meaning of words in relation to one another.
   
3. **Storage of Vectors:**
   - Each paper's vector is stored in a database alongside the PDF. This allows for **fast retrieval** and search results based on the vector comparison during query execution.

#### Pros and Cons of Sentence-BERT:
- **Pros:**
  - Captures the context of words, leading to better semantic search results.
  - Handles synonyms and related terms effectively.
  - Embeddings are robust and adaptable to different contexts.
- **Cons:**
  - Requires significant computational power for vector generation.
  - Large models can be slow for very large datasets.

---

### 2.2 Query Processing and Vectorization

In this step, a user’s **query** is processed and transformed into a form that can be compared with the document vectors. Queries are often short and ambiguous, so they need to be expanded and enriched to retrieve relevant documents.

#### IntelliPaper's Implementation:
1. **Query Vectorization:**
   - Just like documents, user queries are converted into **BERT-based vectors**.
   - We use **Sentence-BERT** for this as well, ensuring that the query's context is captured and it aligns well with the document embeddings.
   
2. **Query Expansion:**
   - We use three methods for **query expansion** to increase the likelihood of retrieving relevant results:
     1. **Synonyms** – Expanding the query with synonyms helps capture different ways of expressing the same concept.
     2. **Contextual Terms** – Expanding based on the context using tools like BERT's pre-trained knowledge.
     3. **Phrases** – Capturing common multi-word phrases and expanding the query with those for more precise matches.
   
3. **Combined Query Vector:**
   - After expansion, we combine the expanded terms with the original query to create a **composite query vector**.

#### Pros and Cons of Query Expansion:
- **Pros:**
  - Increases recall by retrieving documents that might use different terminology than the query.
  - Synonyms and context-aware expansions help retrieve semantically similar documents.
- **Cons:**
  - Can reduce precision by introducing less relevant terms.
  - Query expansion requires careful tuning to avoid overwhelming the search with unrelated results.

---

### 2.3 Document Ranking and Retrieval

Once both the documents and the query are vectorized, we need a way to **rank** documents based on their relevance to the query.

#### IntelliPaper's Hybrid Ranking Approach:
1. **BM25 Algorithm:**
   - BM25 is a **probabilistic IR model** based on term frequency (TF) and document length. It ranks documents based on how many query terms appear in a document and adjusts for the length of the document.
   - **Pros:** Highly effective for short, keyword-based queries and large datasets.
   - **Cons:** Does not capture semantic meaning and relies only on exact keyword matches.
   
2. **Cosine Similarity:**
   - Cosine Similarity is used to measure the **cosine of the angle** between the query vector and the document vector. It evaluates the **semantic similarity** between the two vectors.
   - **Pros:** Excellent at capturing context and meaning, complementing BM25's reliance on exact matches.
   - **Cons:** Computationally intensive and less effective for very large datasets if used alone.

3. **Hybrid Ranking:**
   - In IntelliPaper, we combine both **BM25** and **Cosine Similarity** to create a **hybrid ranking system**. The scores from both methods are weighted (currently 0.5 for each) and combined to produce the final ranking of documents.
   - This hybrid approach balances keyword-based matching (BM25) with context and semantic understanding (Cosine Similarity), providing more **accurate** and **relevant** search results.

4. **Matrix of Vectors:**
   - For each user, a matrix of document vectors is created.
   - We rank the similarity between the **expanded query vector** and each document vector in the matrix.

#### Advantages of Hybrid Ranking:
- **BM25 Pros:** Effective for keyword-based queries and large datasets.
- **Cosine Similarity Pros:** Captures the meaning and context behind words, making it great for semantic search.
- **Hybrid Approach Pros:** By combining both, we ensure that the search engine can handle both exact keyword matches and concept-based queries.
  
---

### 2.4 Evaluation and Optimization

The final step in building an IR system is to evaluate and optimize the system. This is an ongoing process, where search results are analyzed and the system is adjusted for better performance.

#### IntelliPaper’s Future Optimizations:
- **Dynamic Weights:** We are considering adjusting the weights between BM25 and Cosine Similarity (currently 0.5 and 0.5) for specific use cases (e.g., more focus on keywords for technical terms).
- **Caching and Speed Optimization:** To ensure faster searches, we cache document vectors and only re-vectorize new papers that don’t yet have saved vectors.
  
---

## 3. Conclusion

The IntelliPaper search engine combines traditional IR models (like BM25) with modern deep learning techniques (like Sentence-BERT embeddings and Cosine Similarity) to create a **hybrid, context-aware search engine** that provides fast and relevant results.

By focusing on the first five pages of each paper and combining both traditional and contextual retrieval methods, IntelliPaper ensures that users find the most relevant research papers quickly and accurately.

For a more detailed breakdown of how our search engine was built, including examples of query expansion and vectorization, please check our **[Search Engine Documentation](search_engine.md)**.

---

## Appendix: Code Snippet of Search Function

#### `home/views.py`

This part of the search engine handles the core functionality of document vectorization, query expansion, and document ranking based on a hybrid approach of BM25 and cosine similarity.

```python
# home/views.py

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
```

This function expands the query using synonyms, contextual terms, and phrases before calculating document similarity. The vectorized documents and query are ranked using a hybrid approach (BM25 and cosine similarity).

#### `home/helpers.py`

These helper functions handle the expansion of the query by retrieving synonyms, contextual terms, and phrases using tools like NLTK, WordNet, and SpaCy.

```python
# home/helpers.py
from nltk.corpus import wordnet
import nltk
from nltk import ngrams
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np

# nltk.download('wordnet') UNCOMMENT THESE LINE WHEN RUNNING THE SEARCH ENGINE FOR FIRST TIME
# nltk.download('punkt_tab') UNCOMMENT THESE LINE WHEN RUNNING THE SEARCH ENGINE FOR FIRST TIME

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
```

This snippet shows the functions used for expanding the query by:
- **`get_synonyms`**: Fetches synonyms for the query using NLTK's WordNet.
- **`get_contextual_terms`**: Retrieves contextually similar terms using SpaCy's word embeddings.
- **`get_phrases`**: Extracts phrases and named entities from the query using NLTK and SpaCy.

---

For further details on the **hybrid ranking algorithm** and **query expansion**, refer to our [Search Engine Documentation](SEARCH_ENGINE.md).
