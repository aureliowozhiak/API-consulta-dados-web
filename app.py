from flask import Flask, jsonify, request
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import shutil
import random
import json

api_key = None
with open("key", "r") as F:
    api_key = F.read()

app = Flask(__name__)

final_result = {
    "q": "Busca do usuário",
    "url": "https://example.com",
    "url_arquivo": "https://example.com/data.csv",
    "type": "csv",
    "Descrição": "LOREM IMPSUM LOREM IMPSUM LOREM IMPSUM LOREM IMPSUM"
}




@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/html_view")
def html_viewer():
    with open("index.html", "r") as html_file:
        return html_file.read()

def html_writer(html):
    with open("index.html", "w") as html_file:
        html_file.write(html)



def search_google(q):
    query = f"dados completos de {q} filetype:csv"
    url_api = f"https://serpapi.com/search.json?q={query}&location=State+of+Sao+Paulo,+Brazil&hl=pt&gl=br&google_domain=google.com.br&api_key={api_key}"

    response = requests.get(url_api)

    results = response.json()

    # Escreve os resultados formatados em um arquivo JSON
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    for result in results["organic_results"]:
        if result["link"].endswith(".csv"):
            return {"q": q, "csv_link": result["link"]}
    
    return {"q": q, "error": "search not found"}


def search_online(q = None, engine = 'google'):
    match engine:
        case 'google':
            return search_google(q)
        case _:
            return {"result": "engine not found"}
    


@app.route("/search", methods=['GET'])
def search():
    q = request.args.get('q', default = None, type = str)
    data = search_online(q)
    return jsonify(data)



from playwright.sync_api import sync_playwright

