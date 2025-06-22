from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

HF_API_KEY = os.getenv("HF_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "Please enter a message."})

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {
        "inputs": user_message
    }

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            # Get the generated text
            output = response.json()
            if isinstance(output, list):
                bot_reply = output[0]["generated_text"].replace(user_message, "").strip()
            else:
                bot_reply = "Sorry, I didn’t get that."
        else:
            bot_reply = "Model error: " + str(response.status_code)

    except Exception as e:
        print("Error:", e)
        bot_reply = "Server error."

    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


