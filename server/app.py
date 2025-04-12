from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"}), 200

@app.route("/embed-resume", methods=["POST"])
def embed_resume():
    text = request.json.get("text", "")
    # TODO: Replace with Gemini or local model logic
    return jsonify({"skills": ["Python", "SQL", "Excel"]})

if __name__ == "__main__":
    app.run(debug=True, port=5000)