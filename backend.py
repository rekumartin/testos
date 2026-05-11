import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from db import get_students

load_dotenv()

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

PORT = int(os.getenv("PORT", 10000))  

# Format: "key": (lambda function, reverse_boolean)
# True = Ascending (A-Z), False = Descending (Z-A)
SORT_KEYS = {
    "name":      (lambda s: s["name"].lower(),     False),   
    "surname":   (lambda s: s["surname"].lower(),  False),   
    "bioLength": (lambda s: len(s["bio"]),         True),   
}

@app.route("/students")
def students():
    """Vráti zoznam študentov zoradený podľa parametra."""
    sort_by = request.args.get("sort", "name")
    
    # Získame konfiguráciu zoradenia (default na 'name' ak kľúč neexistuje)
    sort_config = SORT_KEYS.get(sort_by, SORT_KEYS["name"])
    key_fn = sort_config[0]
    is_reverse = sort_config[1]

    # Načítanie dát a aplikácia zoradenia
    students_data = get_students()
    data = sorted(students_data, key=key_fn, reverse=is_reverse)
    
    return jsonify(data)

@app.route("/")
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    print(f"Server beží na porte {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)