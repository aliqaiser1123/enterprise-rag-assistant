import os
import streamlit as st


def show_status():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Documents Loaded", len(os.listdir("docs")))
    with col2:
        if st.session_state.documents_loaded:
            st.metric("Collection Status:", "🟢 Ready")
        else:
            st.metric("Collection Status:", "🔴 Not Indexed")
    with col3:
        st.metric("Embedding Model Loaded:", "all-MiniLM-L6-v2")
    with col4:
        st.metric("Large Language Loaded:", "llama-3.3-70b-versatile")
