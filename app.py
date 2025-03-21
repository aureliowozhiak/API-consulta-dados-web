from flask import Flask, jsonify, request
from methods.search import Search

api_key = None
with open("key", "r") as F:
    api_key = F.read()

s = Search(api_key)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
    <h1>API de Consulta de Dados</h1>
    <form action="/search" method="get">
        <label for="q">Digite sua busca:</label>
        <input type="text" id="q" name="q" placeholder="Ex: games">
        <button type="submit">Buscar</button>
    </form>
    <p>Use a rota /search?q=termo para buscar dados diretamente.</p>
    """

@app.route("/search", methods=['GET'])
def search():
    q = request.args.get('q', default = None, type = str)
    data = s.search_online(q.strip().replace(" ", "_").lower())
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)