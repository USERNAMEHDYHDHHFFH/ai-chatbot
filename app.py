from flask import Flask, render_template, request, jsonify
from transformers import pipeline, set_seed

app = Flask(__name__)

# Load GPT-2 locally
generator = pipeline("text-generation", model="gpt2")
set_seed(42)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "Please enter a message."})

    try:
        output = generator(user_message, max_length=60, num_return_sequences=1)
        bot_reply = output[0]["generated_text"].replace(user_message, "").strip()
    except Exception as e:
        print("Local Model Error:", e)
        bot_reply = "Error generating reply."

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
