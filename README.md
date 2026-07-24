# Enterprise RAG Assistant

A production-inspired **Retrieval-Augmented Generation (RAG)** application that allows users to upload multiple documents, generate semantic embeddings, store them in **ChromaDB**, retrieve the most relevant information using semantic search, and generate context-aware answers with **Groq Llama 3.3 70B**.

## ✨ Features

* 📄 Upload PDF, DOCX, and TXT files
* 🧹 Automatic text cleaning
* ✂️ Configurable document chunking
* 🧠 Semantic embeddings with Sentence Transformers
* 🗄️ ChromaDB vector database
* 🔍 Semantic search & Top-K retrieval
* 🤖 RAG-powered AI responses
* 📚 Source citations for every answer
* 💬 Conversation memory
* 🎨 Interactive Streamlit interface

## 🛠️ Tech Stack

* Python
* Streamlit
* ChromaDB
* Sentence Transformers (`all-MiniLM-L6-v2`)
* Groq API
* Llama 3.3 70B Versatile
* PyMuPDF
* python-docx
* Regex

## 🚀 Getting Started

```bash
git clone https://github.com/your-username/Enterprise-RAG-Assistant.git
cd Enterprise-RAG-Assistant
pip install -r requirements.txt
streamlit run app.py
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

## 📌 Skills Demonstrated

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Information Retrieval
* Vector Databases
* Embedding Models
* Prompt Engineering
* LLM Integration
* Python & Streamlit Development

---
## Author
**Muhammad Ali**
*AI Engineer | LLM Engineer | Information Retrieval & RAG Enthusiast*
