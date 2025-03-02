import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/poe/query"

st.title("🤖 Chatbot Poe avec Streamlit")

user_input = st.text_input("Tapez votre message :")

if st.button("Envoyer"):
    if user_input:
        response = requests.post(API_URL, json={"query": user_input})
        st.text_area("Réponse du bot :", response.json().get("response", "Erreur"))
    else:
        st.warning("Veuillez entrer un message !")
