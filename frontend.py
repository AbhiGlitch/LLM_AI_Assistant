import streamlit as st
import requests

st.title("LLM AI Assistant")

question = st.text_input("Enter your question")

if st.button("Send"):
    try:
        response = requests.post(
            "https://llm-ai-backend.onrender.com/ask",
            json={"text": question}
        )

        st.write("You:", question)
        st.write(response.json())
    except Exception as e:
        st.error(f"Error: {e}")