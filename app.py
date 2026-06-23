import requests
import streamlit as st

API_URL = (
    "http://localhost:8000"
)

st.title(
    "RAG Assistant"
)
uploaded_file = (
    st.file_uploader(
        "Upload TXT",
        type=["txt", "pdf", "docx"]
    )
)

if uploaded_file:

    response = requests.post(
        f"{API_URL}/upload",
        files={
            "file":
            (
                uploaded_file.name,
                uploaded_file.getvalue()
            )
        }
    )

    st.json(
        response.json()
    )
question = st.text_input(
    "Ask Question"
)

if st.button(
    "Submit"
):

    response = requests.post(
        f"{API_URL}/ask",
        json={
            "question":
            question
        }
    )

    result = (
        response.json()
    )

    st.write(
        result["answer"]
    )

    st.success(
        f"Source: "
        f"{result['source']}"
    )
