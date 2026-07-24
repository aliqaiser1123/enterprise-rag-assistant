import streamlit as st

from groq import Groq
from dotenv import load_dotenv


def ask_llm(messages, context):
    try:
        load_dotenv()
        client = Groq()
    except Exception as e:
        st.error(str(e))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=messages, temperature=1, top_p=1
    )
    response_text = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.container(height=500):
        for response in st.session_state.messages:
            if response["role"] == "user":
                st.chat_message("User").write(response["content"])

                with st.expander("Expand to see the retrieved context"):
                    for id, chunk, metadata in zip(
                        context["ids"][0],
                        context["documents"][0],
                        context["metadatas"][0],
                    ):
                        st.subheader(f"{id} - Source: {metadata['source']}")
                        st.markdown(chunk.title())
                        st.divider()
            if response["role"] == "assistant":
                st.chat_message("Assistant").write(response["content"])
                with st.expander("See Source"):
                    for distance, metadata in zip(
                        context["distances"][0], context["metadatas"][0]
                    ):
                        st.markdown(
                            f""":green[Chunk:] {metadata["chunk"]}
                            :green[Source:] {metadata["source"]}
                            :green[Distance:] {distance:.4f}"""
                        )
