import streamlit as st
from services.rag_engine import RAGEngine

st.set_page_config(
    page_title="EduBot - Assistant Intelligent pour les Études",
    page_icon="📖",
    layout="wide"
)


# Titre de la page
st.title("📖 Aide - Commandes d'EduBot")

st.markdown("""
<div style="background-color:#f9f9f9; padding:15px; border-radius:10px; border: 1px solid #ddd;">
    <p style="color:r; font-size:20px;">Voici les commandes disponibles dans EduBot pour t'aider à interagir avec l'application :</p>
    <ul>
        <li><span style="color:blue;">**Analyse de PDF**</span> : <span style="color:black;">Upload tes cours pour les résumer. Clique sur le bouton **`[Process PDF]`** après avoir uploader le fichier.</span></li>
        <li><span style="color:blue;">**Questions sur le contenu**</span> : <span style="color:black;">Pose des questions sur tes documents avec la commande: `/askpdf`.</span></li>
                <li><span style="color:red;">- Ex: /askpdf Quelle est la définition de l'ADN ?</span></li>
        <li><span style="color:blue;">**Analyse d'images**</span> : <span style="color:black;">Comprend tes schémas et diagrammes ou autres images. Clique sur le bouton **`[Analyse Image]`** après l'avoir uploader.</span></li>
        <li><span style="color:blue;">**Quiz automatique**</span> : <span style="color:black;">Génère des QCM pour tester tes connaissances avec la commande `/quiz`. </span>
                <li><span style="color:red;">- Ex: /quiz sur les Animaux.</span></li>
        <li><span style="color:blue;">**Mode vocal**</span> : <span style="color:black;">Parle avec EduBot et écoute ses réponses. Utilise l'option **`[Enregistre un message vocal]`** dispo sur le sidebar.</span></li>
        <li><span style="color:blue;">**Fiches de révision**</span> : <span style="color:black;">Crée des fiches personnalisées en image avec la commande `/image`. </span>
                <li><span style="color:red;">- Ex: /image Crée une fiche de révision sur la photosynthèse.</span></li>
        <li><span style="color:blue;">**Recherche sur Internet**</span> : <span style="color:black;">Trouve des informations en ligne avec la commande `/internet`.</span>
                <li><span style="color:red;">- Ex: /internet Quel est le capital de la France ?</span></li>
        <li><span style="color:blue;">**Historique de conversation**</span> : <span style="color:black;">Consulte l'historique de tes échanges avec EduBot.</span></li>
        <li><span style="color:blue;">**Mode sombre**</span> : <span style="color:black;">Vois comment changer le thème de l'application en darkmode en cliquant sur `/darkmode`.</span></li>
        <li><span style="color:blue;">**Mode clair**</span> : <span style="color:black;">Vois comment changer le thème de l'application en lightmode en cliquant sur `/lightmode`.</span></li>
    </ul>
</div>
""", unsafe_allow_html=True)



st.markdown("## 📄 Documentation (README.md)")

try:
    # Lire le fichier README.md
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()

    # Afficher le contenu du README.md
    st.markdown(readme_content)
except FileNotFoundError:
    st.error("Le fichier `README.md` est introuvable. Assurez-vous qu'il est présent dans le répertoire racine du projet.")



# Initialiser le moteur RAG
rag_engine = RAGEngine()

# Indexer le README.md
readme_index_status = rag_engine.process_readme()
if readme_index_status["type"] == "success":
    st.success(readme_index_status["message"])
else:
    st.error(readme_index_status["message"])

# Interface pour poser des questions
st.title("💬 Posez des questions sur le projet")
query = st.text_input("Posez une question sur le README.md :")

if query:
    with st.spinner("Recherche en cours..."):
        response = rag_engine.ask(query, collection_name="readme")
        if response["type"] == "text":
            st.write(response["content"])
        else:
            st.error(response["message"])