from nltk.corpus import wordnet
import nltk
from nltk import ngrams
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np

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