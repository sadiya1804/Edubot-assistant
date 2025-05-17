from api.openai_client import OpenAIClient
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os

class ImageGenerator:
    def __init__(self):
        self.client = OpenAIClient().get_openai_client()
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = "dall-e"
        self.provider = "openai"
        self.api_url = "https://api.openai.com/v1/images/generations"

    def generate(self, prompt):
        st.write(f"Generating image for prompt: /image {prompt}")
        st.session_state.messages.append({"role": "assistant", "content": f"🖼️ Generating image for prompt: {prompt}"})
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url

        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        return image
