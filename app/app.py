from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://ollama:11434/api/chat"

@app.route("/")
def home():
    return "AI Client is running!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen3:4b",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "think": False
        },
        timeout=60
    )

    result = response.json()

    return jsonify({
        "response": result["message"]["content"]
    })

app.run(host="0.0.0.0", port=5000)
