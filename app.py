from flask import Flask, render_template, request, jsonify
from transformers import pipeline, set_seed

app = Flask(__name__)

# Load GPT-2 model (or use 'distilgpt2' for lower memory)
chatbot = pipeline("text-generation", model="distilgpt2")
set_seed(42)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    try:
        result = chatbot(user_input, max_length=100, num_return_sequences=1)
        full_text = result[0]['generated_text']
        bot_reply = full_text[len(user_input):].strip()
        return jsonify({"response": bot_reply})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

