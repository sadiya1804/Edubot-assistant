from api.search_client import SearchClient

class WebSearch:
    def __init__(self):
        self.client = SearchClient()

    def search(self, query):
        try:
            results = self.client.search(query)
            summary = self.client.summarize(results, query)

            return {
                "type": "search_result",
                "summary": summary,
                "sources": [result["url"] for result in results]
            }

        except Exception as e:
            return {"type": "error", "message": f"Erreur lors de la recherche : {str(e)}"}