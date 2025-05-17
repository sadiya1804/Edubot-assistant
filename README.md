# EduBot 🧠📚 – Assistant Intelligent pour l'Éducation

## Contexte du Projet

EduBot est une application interactive conçue pour aider les étudiants à apprendre plus efficacement. Grâce à une interface intuitive et des fonctionnalités avancées, EduBot permet d'analyser des documents, de répondre à des questions, de générer des fiches de révision, et bien plus encore. Ce projet combine des technologies de traitement du langage naturel (NLP), de reconnaissance d'images et d'interfaces utilisateur modernes pour offrir une expérience d'apprentissage personnalisée. 🧑‍🏫🤖

L'application inclut également un mode vocal pour interagir avec EduBot en utilisant la voix, ainsi qu'une fonctionnalité de recherche augmentée pour poser des questions sur des documents spécifiques comme le fichier `README.md`.

---

## 🎯Objectifs

1. ✅**Analyse de documents** : Extraire des informations clés à partir de fichiers PDF ou d'images.
2. ✅**Réponses aux questions** : Répondre aux questions des utilisateurs en utilisant des modèles NLP avancés.
3. ✅**Génération de fiches de révision** : Créer des fiches personnalisées pour faciliter l'apprentissage.
4. ✅**Mode vocal** : Permettre une interaction vocale avec l'application.
5. ✅**Recherche augmentée** : Poser des questions sur des documents spécifiques, comme le fichier `README.md`.
6. ✅**Interface utilisateur intuitive** : Offrir une expérience utilisateur fluide et moderne avec **Streamlit**.

---

## Technologies Utilisées

- **Langage** : Python
- **Framework d'interface utilisateur** : Streamlit
- **Bibliothèques principales** :
  - **OpenAI** : Pour les modèles de génération de texte et d'images.
  - **PyMuPDF (fitz)** : Pour l'extraction de texte à partir de fichiers PDF.
  - **Pillow** : Pour le traitement d'images.
  - **ChromaDB** : Pour la gestion des collections de données et la recherche augmentée.
  - **dotenv** : Pour la gestion des variables d'environnement.
  - **Base64** : Pour l'encodage des fichiers audio.

---

## 🚀Fonctionnalités

### 1. **Analyse de PDF** ✅
- Téléchargez un fichier PDF pour en extraire un résumé ou des informations clés.
- Résumé généré automatiquement et affiché dans l'interface.

### 2. **Analyse d'images** ✅
- Téléchargez une image (JPEG, PNG, etc.) pour analyser son contenu.
- Extraction de texte ou description de l'image.

### 3. **Mode vocal** ✅
- Enregistrez un message vocal directement dans l'application.
- Transcription et traitement du message pour générer une réponse.

### 4. **Génération de fiches de révision** ✅
- Créez des fiches personnalisées en image à partir de commandes spécifiques.

### 5. **Recherche augmentée (RAG)** ✅
- Posez des questions sur des documents spécifiques, comme le fichier `README.md`.
- Utilisation de ChromaDB pour indexer et rechercher dans les documents.

### 6. **Interface utilisateur moderne** ✅
- Interface intuitive avec des thèmes personnalisables (mode clair/sombre).
- Affichage des messages sous forme de chat interactif.

---


## 🧱 Architecture du projet

```
├── app.py                    # Interface principale Streamlit
├── config.py                 # Paramètres de configuration
├── requirements.txt          # Dépendances
├── .env                      # Clés API et variables sensibles
├── README.md                 # Ce fichier ✨
├── core/
│   ├── command_parser.py     # Analyse des requêtes utilisateurs
│   └── session_manager.py    # Gestion des sessions utilisateurs
├── services/
│   ├── pdf_processor.py      # Traitement de documents PDF
│   ├── image_generator.py    # Génération d'aides visuelles
│   ├── image_analyzer.py     # Analyse d’images intégrées
│   ├── web_search.py         # Recherche web éducative
│   ├── audio_processor.py    # Synthèse et transcription audio
│   └── rag_engine.py         # Fonctionnalité RAG (base ChromaDB)
├── api/
│   ├── openai_client.py      # Intégration API OpenAI
│   └── stability_client.py   # API Stable Diffusion (visuels)
└── utils/
    ├── file_handler.py       # Upload & gestion fichiers
    └── text_processor.py     # Nettoyage & segmentations de texte
```


## Étapes du Projet

### 1. Préparation des Données
- Extraction de texte à partir de fichiers PDF avec **PyMuPDF**.
- Traitement des images pour extraire du texte ou des descriptions.

### 2. Développement des Fonctionnalités
- Implémentation des fonctionnalités principales (analyse de PDF, images, mode vocal, etc.).
- Intégration des modèles OpenAI pour la génération de texte et d'images.

### 3. Interface Utilisateur
- Création d'une interface utilisateur avec **Streamlit**.
- Ajout de fonctionnalités interactives comme le chat, le téléchargement de fichiers et les commandes vocales.

### 4. Recherche Augmentée
- Indexation des documents avec **ChromaDB**.
- Implémentation de la recherche augmentée pour répondre aux questions sur des documents spécifiques.

---

## Résultats Obtenus

- **Analyse de documents** : Résumés précis et extraction de texte efficace.
- **Mode vocal** : Interaction fluide avec transcription et réponses en temps réel.
- **Recherche augmentée** : Réponses pertinentes basées sur le contenu des documents indexés.
- **Interface utilisateur** : Expérience utilisateur moderne et intuitive.

---

## Comment Utiliser ce Projet

### 1. Cloner le dépôt
```bash
git clone https://github.com/hafsa223/Chatbot-Multimodal-Intelligent/tree/main
cd Chatbot-Multimodal-Intelligent
```

### 2. Installer les dépendances
Assurez-vous d'avoir Python 3.8 ou une version ultérieure installée. Installez les dépendances avec :
```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement
Créez un fichier `.env` à la racine du projet et ajoutez votre clé API OpenAI :
```
OPENAI_API_KEY=your_openai_api_key
```
OU:

Ajoutez directement votre clé API dans les "" de la variable suivante.

**Dans le fichier openai_client.py**
```bash
self.api_key = os.getenv("OPENAI_API_KEY", "")
```

**Dans le fichier search_client.py**
```bash
self.api_key = os.getenv("SEARCH_API_KEY", "")
```
- **NB: Les deux clés API sont différentes.**

### 4. 📌 Lancer l'application
Exécutez l'application Streamlit avec la commande suivante :
```bash
streamlit run app.py
```

### 5. Utiliser l'application
- **Téléchargez un fichier PDF ou une image** pour l'analyser.
- **Posez des questions** dans la barre de chat.
- **Interagissez en mode vocal** en enregistrant un message.

---

## Exemple de Commandes

- **Analyse de PDF** : Téléchargez un fichier PDF et cliquez sur "Process PDF".
- **Questions sur le contenu** : Posez une question comme `/askpdf Quelle est la définition de l'ADN ?`.
- **Mode vocal** : Enregistrez un message vocal et cliquez sur "Traiter l'audio".
- **Génération de fiches** : Utilisez `/image Crée une fiche de révision sur la photosynthèse`.
- **Recherche augmentée** : Posez une question sur le fichier `README.md` comme "Comment tester ce projet ?".

---

## ✍️ Auteurs

- **NIANG Sadiya**
- **MOUMNI Hafsa**
- **AMOUSSA Mourad**  
 
---


## 📎 Déploiement final

- Front hébergé sur **Streamlit Cloud**
- Projet complet sur Github ✅


## 📚 Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, de le modifier et de le distribuer, sous réserve de conserver la licence d'origine.
