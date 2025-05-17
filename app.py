import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
import base64
from io import BytesIO
import tempfile
from core.command_parser import CommandParser
from core.session_manager import SessionManager
from services.rag_engine import RAGEngine

# Set page config - MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="EduBot - Assistant Intelligent pour les Études",
    page_icon="📚",
    layout="wide"
)


# Load environment variables
load_dotenv()

# Initialize session manager and command parser
@st.cache_resource
def initialize_components():
    session_manager = SessionManager()
    command_parser = CommandParser(session_manager)
    return session_manager, command_parser

session_manager, command_parser = initialize_components()


# Function to autoplay audio
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)


st.markdown("""
<div style="background-color:#4CAF50; padding:15px; border-radius:10px; text-align:center;">
    <h1 style="color:white;">📚 EduBot - Ton Assistant Intelligent pour les Études</h1>
    <p style="color:white; font-size:20px;">EduBot t'aide à apprendre plus efficacement en analysant tes documents de cours,
    en répondant à tes questions et en créant des fiches de révision personnalisées.</p>
</div>
""", unsafe_allow_html=True)



# Sidebar with features
with st.sidebar:

    
    theme_choice = st.radio("Choisir un thème :", ["Light Mode", "Dark Mode"])
    if theme_choice == "Light Mode":
        st.info("Pour activer le mode clair, modifiez le fichier `config.toml` et définissez `[theme] base = 'light'`.")
    elif theme_choice == "Dark Mode":
        st.info("Pour activer le mode sombre, modifiez le fichier `config.toml` et définissez `[theme] base = 'dark'`.")


    # Audio feature section
    st.header("Mode Vocal 🎤")
    
    # Check if audio_input is available in this Streamlit version
    has_audio_input = hasattr(st, 'audio_input')
    
    if has_audio_input:
        # Use audio_input function
        audio_value = st.audio_input("Enregistre un message vocal")
        
        if audio_value:
            st.audio(audio_value)
            if st.button("Traiter l'audio"):
                with st.spinner("Traitement en cours..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                        tmp.write(audio_value.getvalue())
                        tmp_path = tmp.name
                    
                    with open(tmp_path, "rb") as audio_file:
                        response = command_parser.audio_processor.process_audio(audio_file)
                        
                    # Add transcription to chat
                    #st.session_state.messages.append({"role": "user", "content": f"🎤 {response['transcription']}"})
                    st.session_state.messages.append({"role": "assistant", "content": response['response']})
                   
                    # Clean up temp file
                    os.unlink(tmp_path)
                    
                    st.rerun()
    
    # File uploader for PDFs and images
    st.header("Upload de Documents 📄")
    uploaded_file = st.file_uploader("Upload un PDF ou une image", type=["pdf", "jpg", "jpeg", "png"])


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if not uploaded_file and "user_id" not in st.session_state:
    st.session_state.user_id = session_manager.create_session()

# Check if we need to play audio after a rerun
if "play_audio" in st.session_state and st.session_state.play_audio:
    audio_file = st.session_state.play_audio
    autoplay_audio(audio_file)
    # Display audio player as well
    st.audio(audio_file)
    # Clean up
    os.unlink(audio_file)
    del st.session_state.play_audio

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], dict) and "type" in message["content"]:
            # Handle different response types
            if message["content"]["type"] == "image":
                st.image(message["content"]["url"], caption=message["content"]["prompt"])
                st.write(f"Image générée basée sur: {message['content']['prompt']}")
            
            
            elif message["content"]["type"] == "search_result":
                st.write(message["content"]["summary"])
                st.write("Sources:")
            elif message["content"]["type"] == "text":
                st.write(message["content"]["content"])
            
                if "sources" in message["content"]:
                    for source in message["content"]["sources"]:
                        st.write(f"- {source}")
            
            
            elif message["content"]["type"] == "image_analysis":
                st.write(message["content"]["description"])
                if message["content"]["text"]:
                    st.write(f"Texte détecté: {message['content']['text']}")
            
            elif message["content"]["type"] == "pdf_summary":
                st.write(f"Résumé de {message['content']['filename']}:")
                st.write(message["content"]["summary"])
            
            elif message["content"]["type"] == "error":
                st.error(message["content"]["message"])
        else:
            # Regular text message
            st.write(message["content"])

# Process uploaded files
if uploaded_file:
    # Determine file type
    file_type = uploaded_file.name.split('.')[-1].lower()


    # Process based on file type
    if file_type in ['jpg', 'jpeg', 'png', 'gif']:
        with st.chat_message("user"):
            st.write("Uploaded Image")
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing the image..."):
                        #st.session_state.messages.append({"role": "user", "content": f"📷 Image téléchargée: {uploaded_file.name}"})
                    response = command_parser.image_analyzer.analyze(uploaded_file)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    #st.rerun()
    
    
    elif file_type == 'pdf':
        with st.chat_message("user"):
            st.write("Uploaded PDF")
            #st.session_state.messages.append({"role": "assistant", "content": f" Uploaded PDF: {uploaded_file.name}"})

        with st.chat_message("assistant"):
            with st.spinner("Analyzing the PDF..."):
                if st.button("Process PDF"):
                    st.session_state.messages.append({"role": "user", "content": f"📄 Uploaded a PDF: {uploaded_file.name}"})
                    
                    response = command_parser.pdf_processor.process(uploaded_file, user_id=st.session_state.user_id)
                    st.write(response["summary"])
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    #st.rerun()
    
    
# Display chat history
# Chat input
user_input = st.chat_input("Pose ta question à EduBot...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Process the command
    with st.chat_message("assistant"):
        with st.spinner("EduBot réfléchit..."):
            response = command_parser.parse_command(user_input, st.session_state.user_id)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display response
            if isinstance(response, dict) and "type" in response:
                if response["type"] == "image":
                    st.image(response["image"], caption=response["prompt"])
                    st.write(f"Image generated based on: {response['prompt']}")
                    st.session_state.messages.append({"role": "assistant", "content": f"🖼️ Generating image for prompt: {response['prompt']}"})
        
                
                elif response["type"] == "search_result":
                    st.write(response["summary"])
                    st.write("Sources:")
                    for source in response["sources"]:
                        st.write(f"- {source}")
                
                elif response["type"] == "text":  
                    st.write(response["content"])

                elif response["type"] == "error":
                    st.error(response["message"])
            else:
                st.write(response)
