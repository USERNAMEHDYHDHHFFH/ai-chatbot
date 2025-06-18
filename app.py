from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Or use other model
API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    payload = {
        "inputs": user_input,
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        generated_text = response.json()[0]["generated_text"]
        reply = generated_text[len(user_input):].strip()
    except Exception as e:
        reply = "Sorry, something went wrong."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

