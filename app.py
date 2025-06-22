from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Directly use the working GPT-2 model
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {os.environ.get('HF_API_KEY')}"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": user_message},
        timeout=15
    )

    if response.status_code == 200:
        try:
            result = response.json()
            generated = result[0]["generated_text"]
            reply = generated.replace(user_message, "").strip()
        except Exception:
            reply = "Couldn't parse model response."
    else:
        reply = f"Model error: {response.status_code}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


