from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/gpt2"  # You can switch to any free HF model
HEADERS = {"Authorization": f"Bearer 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"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    data = {"inputs": user_message}
    response = requests.post(API_URL, headers=HEADERS, json=data)
    result = response.json()
    
    try:
        bot_reply = result[0]["generated_text"]
    except Exception:
        bot_reply = "Sorry, something went wrong."

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)

