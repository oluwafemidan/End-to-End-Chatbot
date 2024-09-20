#from dotenv import load_dotenv
#load_dotenv()  # Load environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Q&A Demo")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.header("Gemini Conversational AI ")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and user_input:
    with st.spinner("Processing..."):  # Add a loading animation
        response = get_gemini_response(user_input)
        st.session_state['chat_history'].append(("You", user_input))
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("The Chat history is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
