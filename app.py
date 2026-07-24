import os
import streamlit as st

from utils.llm import ask_llm
from utils.cleaner import clean_data
from utils.chunker import chunk_data
from utils.status import show_status
from utils.retriever import retrieve_data
from utils.file_loader import load_files, extract_data
from sentence_transformers import SentenceTransformer
from utils.embeddings import generate_embeddings, store_embeddings


@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "status" not in st.session_state:
    st.session_state.status = False

if "database_created" not in st.session_state:
    st.session_state.database_created = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "temp_memory" not in st.session_state:
    st.session_state.temp_memory = []

st.set_page_config(page_title="Enterprise RAG Assistant", layout="wide")

st.title("Enterprise :green[RAG] Assistant", text_alignment="center")
st.markdown(
    ":green[Enterprise RAG Assistant] is a production-inspired Retrieval-Augmented Generation (RAG) application that enables users to upload multiple documents, generate semantic embeddings, store them in a ChromaDB vector database, retrieve the most relevant information using semantic search, and generate context-aware answers using Large Language Models (LLMs). The system supports metadata filtering, source citations, conversational memory, and an intuitive Streamlit interface for intelligent document-based question answering.",
    text_alignment="center",
)
st.divider()

with st.sidebar:
    if st.button(":red[Clear Chat]"):
        st.session_state.messages = []
        st.success("Chat messages cleared, Start new chat")

uploaded_files = st.file_uploader(
    "Upload your files",
    accept_multiple_files=True,
    type=[".pdf", ".txt", ".doc", ".docx"],
)

if st.button("Upload"):
    if uploaded_files:
        load_files(uploaded_files)
        st.success("Document Successfully uploaded to system")
    else:
        st.session_state.documents_loaded = False
        st.session_state.status = False
        st.error("Upload your files first")
else:
    pass


if st.session_state.documents_loaded:
    show_status()

    chunks = []
    chunk_ids = []
    documents = []
    metadatas = []

    col1, col2, col3, col4 = st.columns([6, 3, 3, 3])

    with col1:
        query = st.text_input("Enter your query:")

    with col2:
        chunk_size = st.slider(
            "Select your chunk size:", min_value=100, max_value=2000, value=500, step=50
        )
    with col3:
        overlap = st.slider(
            "Select chunk overlap size:",
            min_value=10,
            max_value=200,
            value=100,
            step=10,
        )

    for file in os.listdir("docs"):
        documents.append(extract_data(f"docs/{file}"))

    cleaned_data = clean_data(documents)
    chunked_data = chunk_data(cleaned_data, chunk_size, overlap)

    for doc in chunked_data:
        for source, data in doc.items():
            for index, chunk in enumerate(data):
                chunks.append(chunk)
                metadatas.append({"source": source, "chunk": index + 1})
    for id in range(len(chunks)):
        chunk_ids.append(f"Chunk_{id + 1}")

    if not st.session_state.database_created:
        with st.spinner("Creating Vector Database ..."):
            embeddings = generate_embeddings(model, chunks)
            st.session_state.database = store_embeddings(
                chunk_ids, chunks, embeddings, metadatas
            )
        st.success("Database Created Successfully")
    else:
        st.markdown(":green[Vector Database Activated]")

    st.session_state.temp_memory = st.session_state.messages[:]

    with col4:
        no_of_chunks_retrieval = st.slider(
            "No. of chunks to retrieve:",
            min_value=1,
            max_value=len(chunks),
            value=5,
            step=1,
        )

    if st.button("SUBMIT"):
        if query:
            with st.spinner("Generating response ..."):
                context = retrieve_data(
                    model, query, st.session_state.database, no_of_chunks_retrieval
                )
                augmented_query = f"""You are an expert AI assistant. Answer according to the supplied context. If the answer cannot be found, Reply:"I couldn't find that information in the uploaded documents."Context: {"\n\n".join(context["documents"][0])} Query:"""
                st.session_state.messages.append({"role": "user", "content": query})
                st.session_state.temp_memory.append(
                    {"role": "user", "content": augmented_query}
                )
                ask_llm(st.session_state.temp_memory, context)
        else:
            st.warning("Enter query first")
else:
    pass
