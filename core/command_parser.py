from services.visual_aid_generator import ImageGenerator
from services.edu_search import WebSearch
from services.image_analyzer import ImageAnalyzer
from services.pdf_processor import PDFProcessor
from services.audio_processor import AudioProcessor
from services.rag_engine import RAGEngine


class CommandParser:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.image_generator = ImageGenerator()
        self.web_search = WebSearch()
        self.image_analyzer = ImageAnalyzer()
        self.pdf_processor = PDFProcessor(session_manager=session_manager)
        self.audio_processor = AudioProcessor()
        self.rag_engine = RAGEngine()

    def parse_command(self, user_input, user_id, file=None):
        """Parse user input and route to appropriate service"""
        
        # Educational commands
        if user_input.startswith("/quiz "):
            topic = user_input[6:].strip()
            return f"Voici un quiz sur {topic}:\n\n" + self._generate_quiz(topic)
            
        
        # Handle image generation command
        elif user_input.startswith("/image "):
            prompt = user_input[7:].strip()
            return self.image_generator.generate(prompt)
            
        # Handle web search command
        elif user_input.startswith("/internet "):
            query = user_input[10:].strip()
            return self.web_search.search(query)

        elif user_input.startswith("/clear"):
            self.session_manager.clear_session(user_id)
            return {"type": "success", "message": "Session cleared."}

        elif user_input.startswith("/askpdf "):
            question = user_input[8:].strip()
            uploaded_pdf = self.session_manager.sessions.get(user_id, {}).get("last_file")
            if uploaded_pdf and uploaded_pdf.name.endswith(".pdf"):
                collection_name = uploaded_pdf.name.replace(".pdf", "")
                response = self.rag_engine.ask(question, collection_name)
                #print("✅ Réponse renvoyée par RAG:", response)
                return response
            return {"type": "error", "message": "Aucun PDF n'a encore été traité pour cette session."}



        # Handle file uploads
        elif file is not None:
            file_type = file.filename.split('.')[-1].lower()
            
            # Image analysis
            if file_type in ['jpg', 'jpeg', 'png', 'gif']:
                return self.image_analyzer.analyze(file)
                
            # PDF processing
            elif file_type == 'pdf':
                return self.pdf_processor.process(file)
                
        # Default educational assistant response
        else:
            from api.openai_client import OpenAIClient
            openai_client = OpenAIClient()
            return openai_client.generate_response(
                user_input,
                system_prompt="Tu es EduBot, un assistant éducatif intelligent. Tu aides les étudiants à comprendre des concepts, à réviser et à apprendre efficacement. Donne des explications claires, concises et pédagogiques."
            )

    def _generate_quiz(self, topic):
        """Generate a quiz on the given topic"""
        from api.openai_client import OpenAIClient
        openai_client = OpenAIClient()
        prompt = f"Crée un quiz de 5 questions à choix multiples sur le sujet: {topic}. Pour chaque question, fournis 4 options et indique la bonne réponse."
        return openai_client.generate_response(prompt)

