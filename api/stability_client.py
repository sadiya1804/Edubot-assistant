import os
import requests
import base64
import json

class StabilityClient:
    def __init__(self):
        self.api_key = os.getenv("STABILITY_API_KEY")
        self.api_host = os.getenv("STABILITY_API_HOST", "https://api.stability.ai")
        
    def generate_image(self, prompt, height=1024, width=1024, steps=30):
        """Generate an image using Stable Diffusion"""
        if not self.api_key:
            raise ValueError("Missing Stability API key")
            
        url = f"{self.api_host}/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "text_prompts": [
                {
                    "text": prompt,
                    "weight": 1.0
                }
            ],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": steps
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Stability API error: {response.status_code} - {response.text}")
            
        data = response.json()
        
        # Get the base64 image
        image_b64 = data["artifacts"][0]["base64"]
        
        # For Streamlit, we can return the base64 data directly
        return f"data:image/png;base64,{image_b64}"
