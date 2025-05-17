import os
import streamlit as st  
import fitz  # PyMuPDF
from api.openai_client import OpenAIClient
import re

# 👇 Forcer ChromaDB à utiliser pysqlite3 à la place de sqlite3
try:
    import pysqlite3
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

import chromadb
from chromadb.config import Settings

class RAGEngine:
    def __init__(self, collection_dir="./chromadb"):
        self.client = chromadb.Client(Settings(anonymized_telemetry=False, is_persistent=False))
        self.openai = OpenAIClient()

    def process_pdf(self, pdf_file, collection_name):
        os.makedirs("uploaded", exist_ok=True)
        pdf_path = os.path.join("uploaded", pdf_file.name)

        with open(pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        try:
            # Extraction texte avec PyMuPDF
            doc = fitz.open(pdf_path)
            chunks = [page.get_text() for page in doc if page.get_text().strip() != ""]
            doc.close()
        except Exception as e:
            return {"type": "error", "message": f"Erreur extraction texte : {str(e)}"}

        try:
            collection = self.client.get_or_create_collection(collection_name)
            ids = [f"{pdf_file.name}_{i}" for i in range(len(chunks))]
            collection.add(documents=chunks, ids=ids)
            st.write(f"✅ Collection '{collection_name}' ajoutée avec {len(chunks)} chunks.")


        except Exception as e:
            return {"type": "error", "message": f"Erreur ajout dans Chroma : {str(e)}"}

        return {"type": "pdf_summary", "filename": pdf_file.name, "summary": "Document indexé avec succès pour RAG."}

    def ask(self, query, collection_name="default"):
        if not re.match(r'^[a-zA-Z]+$', collection_name):
            return {"type": "error", "message": "Le nom de la collection ne doit contenir que des lettres (sans caractères spéciaux ou chiffres)."}

        try:
            # Récupérez la collection
            collection = self.client.get_collection(collection_name)
            results = collection.query(query_texts=[query], n_results=3)
            docs = results["documents"][0]
        except Exception as e:
            return {"type": "error", "message": f"Erreur RAG : {str(e)}"}

        context = "\n\n".join(docs)
        prompt = f"Voici des extraits du document :\n{context}\n\nRéponds à la question suivante : {query}"

        try:
            response = self.openai.generate_response(prompt)
        except Exception as e:
            return {"type": "error", "message": f"Erreur appel OpenAI : {str(e)}"}

        return {"type": "text", "content": response}


    def process_readme(self, readme_path="README.md", collection_name="readme"):
        """
        Indexe le contenu du README.md pour permettre des questions dessus.
        """
        if not os.path.exists(readme_path):
            return {"type": "error", "message": f"Le fichier {readme_path} est introuvable."}

        try:
            # Lire le contenu du README.md
            with open(readme_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Diviser le contenu en chunks (par exemple, par paragraphes)
            chunks = content.split("\n\n")  # Divise par double saut de ligne

            # Créer ou récupérer la collection
            collection = self.client.get_or_create_collection(collection_name)
            ids = [f"{collection_name}_{i}" for i in range(len(chunks))]
            collection.add(documents=chunks, ids=ids)

            return {"type": "success", "message": f"README.md indexé avec succès dans la collection '{collection_name}'."}

        except Exception as e:
            return {"type": "error", "message": f"Erreur lors de l'indexation du README.md : {str(e)}"}
