import os
import requests
from api.openai_client import OpenAIClient

class SearchClient:
    def __init__(self):
        self.api_key = os.getenv("SEARCH_API_KEY")
        self.search_engine_id = os.getenv("SEARCH_ENGINE_ID")
        self.openai_client = OpenAIClient()
   
    def search(self, query, num_results=5):
        """Search the web using Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": num_results,
            "gl": "fr",  
            "hl": "fr"   
        }

        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Search API error: {response.status_code}")
            
        results = response.json()
        
        search_results = []
        if "items" in results:
            for item in results["items"]:
                search_results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "url": item.get("link", "")
                })
                
        return search_results
  
    def summarize(self, search_results, query):
        """Summarize search results using OpenAI"""
        formatted_results = ""
        for i, result in enumerate(search_results):
            formatted_results += f"Résultat {i+1}:\nTitre: {result['title']}\nExtrait: {result['snippet']}\nURL: {result['url']}\n\n"
        
        prompt = (
            f"Tu es un assistant intelligent. J'ai effectué une recherche web sur : '{query}'. "
            f"Voici les extraits trouvés :\n\n{formatted_results}\n\n"
            f"En te basant uniquement sur ces résultats, réponds clairement à la question : '{query}'. "
            f"Si certains résultats sont hors sujet, ignore-les. Fournis aussi les liens utiles."
        )

        summary = self.openai_client.generate_response(prompt)
        return summary