from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
import os

load_dotenv()  # Load .env variables

app = Flask(__name__)

HF_API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}


app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {os.getenv('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')}"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "No message received."})

    payload = {"inputs": user_message}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return jsonify({"reply": result[0]["generated_text"]})
        else:
            return jsonify({"reply": "Sorry, something went wrong."})
    except Exception as e:
        return jsonify({"reply": "API error."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

