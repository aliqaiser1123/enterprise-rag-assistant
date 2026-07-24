import os
import fitz
import streamlit as st

from docx import Document


def load_files(uploaded_files):
    os.makedirs("docs", exist_ok=True)
    for file in os.listdir("docs"):
        os.remove(f"docs/{file}")
    for file in uploaded_files:
        with open(f"docs/{file.name}", "wb") as f:
            f.write(file.getbuffer())
    st.session_state.documents_loaded = True
    st.session_state.status = True
    st.session_state.database_created = False


def read_pdf(path):
    data = ""
    with fitz.open(path) as pdf:
        for page in pdf:
            data += page.get_text() + "\n"
    return {path.replace("docs/", ""): [data]}


def read_doc(path):
    data = ""
    doc = Document(path)
    for para in doc.paragraphs:
        data += para.text + "\n"
    return {path.replace("docs/", ""): [data]}


def read_txt(path):
    data = ""
    with open(path, "r", encoding="utf-8") as f:
        data += f.read()
    return {path.replace("docs/", ""): [data]}


def extract_data(path):
    extension = os.path.splitext(path)[1].lower()

    if extension == ".pdf":
        return read_pdf(path)
    elif extension == ".txt":
        return read_txt(path)
    elif extension in [".doc", ".docx"]:
        return read_doc(path)
    else:
        raise ValueError("Unsupported file")
