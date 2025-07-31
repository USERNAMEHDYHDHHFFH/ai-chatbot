from flask import Flask, render_template, request, jsonify
import requests, os
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
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                bot_reply = result[0]["generated_text"].replace(user_message, "").strip()
            else:
                bot_reply = "Empty or invalid response."
        elif response.status_code == 503:
            bot_reply = "Model is warming up. Try again shortly."
        elif response.status_code == 404:
            bot_reply = "Model not found. Check URL or permissions."
        else:
            bot_reply = f"Model error: {response.status_code} - {response.text}"

    except Exception as e:
        print("API Exception:", e)
        bot_reply = "Server error."

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

