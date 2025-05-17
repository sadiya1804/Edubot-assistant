from api.openai_client import OpenAIClient
import streamlit as st
import requests
import base64

    
class ImageAnalyzer:
    def __init__(self):
        self.openai_client = OpenAIClient().get_openai_client()
        self.model = "gpt-4o-mini"
        self.provider = "openai"
    

    def analyze(self, image_file):
        
        if st.button("Analyze Image"):
            client = self.openai_client

            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

            response = client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            { "type": "input_text", "text": "Que contient cette image?" },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        ],
                    }
                ],
            )
            return(response.output_text)