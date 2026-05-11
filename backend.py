import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from db import get_students

load_dotenv()

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

PORT = int(os.getenv("PORT", 10000))  

SORT_KEYS = {
    "name":      (lambda s: s["name"].lower(),     True),   
    "NAME":      (lambda s: s["name"].lower(),    False),  
    "surname":   (lambda s: s["surname"].lower(),  True),   
    "SURNAME":   (lambda s: s["surname"].lower(), False),
    "bioLength": (lambda s: len(s["bio"]),         True),   
    "BIOLENGTH": (lambda s: len(s["bio"]),        False),

}


@app.route("/students")
def students():
    """
    Vráti zoznam študentov ako JSON.

    Query parametre:
      ?sort=name       – zoradenie podľa mena (predvolené)
      ?sort=surname    – zoradenie podľa priezviska
      ?sort=bioLength  – zoradenie podľa dĺžky bio
    """
    sort_by = request.args.get("sort", "name")
    key_fn = SORT_KEYS.get(sort_by, SORT_KEYS["name"])

    data = sorted(get_students(), key=key_fn)
    return jsonify(data)


@app.route("/")
def index():
    """Obsluží hlavnú HTML stránku."""
    return app.send_static_file("index.html")


if __name__ == "__main__":
    print(f" Server beží na porte {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
