import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import json
import openai

# Configuration de l'interface
st.set_page_config(page_title="Web Scraper", layout="wide")

# Titre de l'application avec une meilleure mise en forme
st.title("🔍 Web Scraper avec IA et Streamlit")
st.markdown("### Extraire et analyser intelligemment des informations depuis une page web")

# Mise en place des colonnes pour afficher les menus
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    # Entrée pour l'URL
    url = st.text_input("🌍 Entrez l'URL du site web à scraper :", placeholder="https://exemple.com")

with col2:
    # Menu déroulant pour choisir une fonctionnalité standard
    option = st.selectbox(
        "📌 Choisissez une fonctionnalité :",
        ["Afficher le titre", "Afficher tout le texte", "Afficher toutes les balises H1",
         "Afficher tous les paragraphes",
         "Afficher tous les liens", "Afficher toutes les images", "Afficher le nombre total de mots",
         "Afficher les métadonnées",
         "Extraire les numéros de téléphone", "Extraire les adresses e-mail",
         "Premium - Analyser la structure HTML", "Premium - Extraire les hashtags", "Premium - Analyser le SEO",
         "Premium - Détecter les réseaux sociaux", "Premium - Exporter en JSON"]
    )

with col3:
    # Menu déroulant pour choisir une fonctionnalité IA
    option_ai = st.selectbox(
        "🤖 Fonctionnalités IA :",
        ["Aucune", "Résumé automatique", "Analyse de sentiment", "Classification du contenu",
         "Détection des entités nommées", "Génération de mots-clés"]
    )
    start_button = st.button("Lancer l'analyse")

if start_button and url:
    try:
        # Requête HTTP pour obtenir le contenu de la page
        response = requests.get(url)
        response.raise_for_status()

        # Parsing du contenu avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()

        with col1:
            # Exécution de la fonctionnalité standard sélectionnée
            if option == "Afficher le titre":
                st.subheader("📌 Titre de la page")
                st.write(soup.title.string if soup.title else "Titre non trouvé")

            elif option == "Afficher tout le texte":
                st.subheader("📃 Contenu de la page")
                st.text_area("Texte extrait", page_text, height=300)

            elif option == "Afficher toutes les balises H1":
                headers = [h1.get_text() for h1 in soup.find_all('h1')]
                st.subheader("📑 Balises H1")
                st.write(headers)

            elif option == "Afficher tous les paragraphes":
                paragraphs = [p.get_text() for p in soup.find_all('p')]
                st.subheader("📄 Paragraphes")
                st.write(paragraphs)

            elif option == "Afficher tous les liens":
                links = [a['href'] for a in soup.find_all('a', href=True)]
                st.subheader("🔗 Liens")
                st.write(links)

            elif option == "Afficher toutes les images":
                images = [img['src'] for img in soup.find_all('img', src=True)]
                st.subheader("🖼️ Images")
                st.write(images)

            elif option == "Afficher le nombre total de mots":
                word_count = len(page_text.split())
                st.subheader("🔢 Nombre total de mots")
                st.write(f"Nombre total de mots : {word_count}")

            elif option == "Afficher les métadonnées":
                meta_tags = {meta.get('name', 'N/A'): meta.get('content', 'N/A') for meta in soup.find_all('meta')}
                st.subheader("📜 Métadonnées")
                st.write(meta_tags)

        with col1:
            # Exécution de la fonctionnalité IA sélectionnée
            if option_ai != "Aucune":
                st.subheader(f"🤖 Analyse IA : {option_ai}")
                openai.api_key = "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"  # Ma clé API OpenAI

                if option_ai == "Résumé automatique":
                    prompt = f"Résumé du texte suivant : {page_text[:2000]}"
                    response = openai.Completion.create(engine="gpt-3.5-turbo", prompt=prompt, max_tokens=100)
                    st.write(response["choices"][0]["text"].strip())

                elif option_ai == "Analyse de sentiment":
                    prompt = f"Analyse du sentiment du texte suivant : {page_text[:2000]}"
                    response = openai.Completion.create(engine="gpt-3.5-turbo", prompt=prompt, max_tokens=50)
                    st.write(response["choices"][0]["text"].strip())

                elif option_ai == "Classification du contenu":
                    prompt = f"Classifie le texte suivant dans une des catégories suivantes : actualités, blog, produit, recherche, autre. Texte : {page_text[:2000]}"
                    response = openai.Completion.create(engine="gpt-3.5-turbo", prompt=prompt, max_tokens=50)
                    st.write(response["choices"][0]["text"].strip())

                elif option_ai == "Détection des entités nommées":
                    prompt = f"Identifie les entités nommées dans ce texte : {page_text[:2000]}"
                    response = openai.Completion.create(engine="gpt-3.5-turbo", prompt=prompt, max_tokens=100)
                    st.write(response["choices"][0]["text"].strip())

                elif option_ai == "Génération de mots-clés":
                    prompt = f"Génère des mots-clés pertinents pour le texte suivant : {page_text[:2000]}"
                    response = openai.Completion.create(engine="gpt-3.5-turbo", prompt=prompt, max_tokens=50)
                    st.write(response["choices"][0]["text"].strip())

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erreur lors de la récupération de la page : {e}")
    except Exception as e:
        st.error(f"⚠️ Une erreur est survenue : {e}")
