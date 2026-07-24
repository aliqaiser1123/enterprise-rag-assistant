import chromadb
import streamlit as st


def generate_embeddings(model, chunks):
    return model.encode(chunks)


def store_embeddings(ids, documents, embeddings, metadatas):
    client = chromadb.PersistentClient(path="./database")
    try:
        client.delete_collection("embeddings")
    except Exception:
        pass
    database = client.get_or_create_collection("embeddings")
    database.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
    )
    st.session_state.database_created = True
    return database
