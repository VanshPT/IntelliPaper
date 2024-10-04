# 📚 IntelliPaper: Your Ultimate Research Buddy!

IntelliPaper is a powerful web application designed for individuals who regularly read and study research articles. With a suite of intelligent features, it simplifies the academic reading experience, allowing users to efficiently manage their research papers and notes. Whether you're a student, researcher, or academic, IntelliPaper is here to be your best friend in your journey of knowledge! 🌟

---

## 🚀 Features

- **📄 Easy Paper Upload:** Upload your downloaded research papers effortlessly. IntelliPaper automatically extracts essential metadata, including the title, authors, and abstract, and securely stores your papers.

- **🤖 AI-Powered Auto Clustering:** Using advanced AI algorithms, all your research papers are automatically clustered into organized folders, making access a breeze!

- **🗂️ Custom Readlists:** Create, modify, and manage your own readlists. Add or remove papers to tailor your research experience!

- **📖 Embedded Article Viewer:** Each saved article opens in an embedded format, providing options for local downloads and easy access.

- **📝 User-Friendly Note Taking:** Write and save notes using the TinyMCE editor in a familiar word-like format. Your notes are always preserved, making it easy to refer back when needed. You can even download your notes as a Word file! 

- **⏳ Summary Generator:** Get a concise summary of any research paper in just seconds with our GenAI-powered summary generator, saving you valuable time.

- **🤖 RAG-Based Chatbot:** Ask questions about your saved papers! (This feature is currently under construction.)

- **🔍 Custom Search Engine:** A robust search engine built from scratch that retrieves research papers based on contextual relevance, using advanced NLP and IR systems. Our search algorithm ranks papers based on a hybrid approach using BM25 and Cosine Similarity to ensure the best results for your query. For more details, check out our Search Engine Documentation! 🚀 refer to our [Search Engine Documentation](SEARCH_ENGINE.md).

---

## 🛠️ Tech Stack

- **Backend:** Django
- **Frontend:** Jinja templating, HTML, CSS, JavaScript
- **External APIs:** 
  - Gemini-1.5-Flash (for GenAI capabilities)
  - TinyMCE editor (for note-taking)
- **Core Technologies:** 
  - Natural Language Processing (NLP)
  - Information Retrieval (IR)
  - Agglomerative Clustering (for AI clustering)
  - BERT Embeddings (for context-aware vectors)

---

## 📦 Installation Instructions

To run IntelliPaper locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/intellipaper.git
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   cd intellipaper
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` File:**
   In the root folder, create a `.env` file and add your API keys in the following format:
   ```plaintext
   GEMINI_API_KEY='your-gemini-api-key' 
   TINY_MCE_EDITOR='your-tinymce-api-key'
   ```

5. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser
   ```
   
7. **(Search Engine setup) uncomment all lines in views.py and helper.py with syntax nltk.download(*) when using the search engine for the first time. After all resources are downloaded once in your system for 'punkt_tab' and 'wordnet':**
   This (example)
   ```bash
   # nltk.download('wordnet') UNCOMMENT THESE LINE WHEN RUNNING THE SEARCH ENGINE FOR FIRST TIME
   # nltk.download('punkt_tab') UNCOMMENT THESE LINE WHEN RUNNING THE SEARCH ENGINE FOR FIRST TIME
   ```
   to this (comment all such lines in both files after resources are downloaded once for your search engine to work properly)
   ```bash
   nltk.download('wordnet')
   nltk.download('punkt_tab')
   ```
8. **Again Comment out all lines with syntax nltk.download(*) after all resources are downloaded in system.(Important)**
   
9. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```

Now you're ready to enjoy IntelliPaper! 🎉

---

## 🧰 Technologies Used

- **Natural Language Processing (NLP):** Employed for metadata extraction and content analysis.
- **Information Retrieval (IR):** Utilized in the custom search engine for effective paper querying.
- **BERT based Embeddings:** Used to generate context-aware vectors for better clustering of papers.
- **Agglomerative Clustering:** Machine learning algorithm for clustering research papers into coherent groups.

---

IntelliPaper aims to be the most effective AI/GenAI project for enhancing research article reading and studying. Experience a new level of efficiency and organization in your academic journey with IntelliPaper! 🌈

---

👨‍💻 App developed by Vansh Thakkar

---
## Some Screeshots
![image](https://github.com/user-attachments/assets/6c86c8b1-1619-4466-9fe2-8c5ecbb4425c)
![image](https://github.com/user-attachments/assets/b0eeeabb-f830-49a6-94f4-205664201c5d)
![image](https://github.com/user-attachments/assets/d85a1937-c640-43f5-adba-ee7f34946984)
![image](https://github.com/user-attachments/assets/3289cce9-eb9d-4551-86fd-29c3fbe351a0)
![image](https://github.com/user-attachments/assets/4fc6e05e-b9fa-4c8b-9c81-9b4f1d3c6078)
![image](https://github.com/user-attachments/assets/432b2d5b-85b8-4827-ab30-16c73d011fe1)
![image](https://github.com/user-attachments/assets/044e9cfb-f8f9-4f49-b5a0-8d1eeb56e74e)
![image](https://github.com/user-attachments/assets/e8bc6c00-ba69-4b2a-b91b-c248cecdced7)
![image](https://github.com/user-attachments/assets/67efb429-5517-4a40-8da6-0fa143e74572)
![image](https://github.com/user-attachments/assets/1e35511c-803b-413d-b02d-a5a84870f2ca)




