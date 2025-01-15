import streamlit as st
import pandas as pd
import pywhatkit as kit
import time
import os

st.title("Automatisation des messages WhatsApp")
st.subheader("Envoyez des messages WhatsApp à plusieurs contacts")

# Option pour choisir entre fichier Excel ou saisie manuelle
option = st.radio(
    "Choisissez comment fournir les numéros de téléphone :",
    ("Télécharger un fichier Excel", "Saisir les numéros manuellement")
)

# Initialisation des numéros
phone_numbers = []

if option == "Télécharger un fichier Excel":
    uploaded_file = st.file_uploader("Téléchargez un fichier Excel", type=["xlsx", "xls"])
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Aperçu des données téléchargées :")
            st.dataframe(df.head())

            # Chercher la première colonne contenant des numéros
            df.columns = df.columns.str.strip()
            phone_column = st.selectbox("Choisissez la colonne contenant les numéros :", df.columns)
            phone_numbers = df[phone_column].dropna().astype(str).tolist()
            st.success(f"{len(phone_numbers)} numéros détectés.")
        except Exception as e:
            st.error(f"Erreur lors du traitement du fichier : {e}")

elif option == "Saisir les numéros manuellement":
    manual_numbers = st.text_area(
        "Entrez les numéros de téléphone, séparés par une virgule ou un retour à la ligne :",
        placeholder="+1234567890, +1987654321"
    )
    if manual_numbers:
        # Convertir en liste de numéros
        phone_numbers = [num.strip() for num in manual_numbers.replace("\n", ",").split(",") if num.strip()]
        st.success(f"{len(phone_numbers)} numéros saisis.")

# Message personnalisé
message = st.text_area("Entrez le message à envoyer", placeholder="Écrivez votre message ici")

# Sélection de l'heure et des minutes
heure = st.number_input("Heure (24h)", min_value=0, max_value=23, step=1, value=12)
minute = st.number_input("Minute", min_value=0, max_value=59, step=1, value=30)

# Bouton pour envoyer les messages
if st.button("Envoyer les messages"):
    if not phone_numbers:
        st.error("Aucun numéro détecté. Veuillez télécharger un fichier ou saisir les numéros manuellement.")
    elif not message:
        st.error("Veuillez entrer un message.")
    else:
        st.info("Envoi des messages en cours...")
        try:
            for numero in phone_numbers:
                st.write(f"Envoi du message à {numero}...")

                # Envoi du message avec pywhatkit
                kit.sendwhatmsg(numero, message, heure, minute)
                time.sleep(20)  # Temps pour WhatsApp Web de se charger

            st.success("Tous les messages ont été envoyés avec succès !")
        except Exception as e:
            st.error(f"Une erreur s'est produite : {e}")
