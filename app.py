from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

HF_MODEL_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "Please enter a message."})

    try:
        response = requests.post(
            HF_MODEL_URL,
            headers=headers,
            json={"inputs": user_message},
            timeout=15
        )
        # Debug logging
        print("Status:", response.status_code, "Response:", response.text[:200])

        if response.status_code == 200:
            result = response.json()
            bot_reply = result[0]["generated_text"].replace(user_message, "").strip()
        else:
            bot_reply = f"Model error: {response.status_code}"

    except Exception as e:
        print("API Exception:", e)
        bot_reply = "Server error."

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

