import requests
import json
import os
class Search:
    def __init__(self, api_key):
        self.api_key = api_key

        
    final_result = {
        "q": "Busca do usuário",
        "url": "https://example.com",
        "url_arquivo": "https://example.com/data.csv",
        "type": "csv",
        "Descrição": "LOREM IMPSUM LOREM IMPSUM LOREM IMPSUM LOREM IMPSUM"
    }

    def convert_json_to_result(self, results, q, type):
        for result in results["organic_results"]:
            if result["link"].endswith(".csv"):
                return {"q": q, "csv_link": result["link"], "type": type}
        
        return {"q": q, "error": "search not found"}

    def search_google(self, q, type):
        query = f"dados completos de {q} filetype:csv"
        url_api = f"https://serpapi.com/search.json?q={query}&location=State+of+Sao+Paulo,+Brazil&hl=pt&gl=br&google_domain=google.com.br&api_key={self.api_key}"

        response = requests.get(url_api)

        results = response.json()

        # Escreve os resultados formatados em um arquivo JSON
        with open(f"methods/{q}.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
    
        return self.convert_json_to_result(results, q, type)


    def search_online(self, q = None, engine = 'google'):

        if q is None:
            return {"result": "search not found"}
        
        # verifica se o arquivo existe
        if os.path.exists(f"methods/{q}.json"):
            with open(f"methods/{q}.json", "r", encoding="utf-8") as f:
                return self.convert_json_to_result(json.load(f), q, "arquivo local")

        match engine:
            case 'google':
                return self.search_google(q, "google")
            case _:
                return {"result": "engine not found"}

