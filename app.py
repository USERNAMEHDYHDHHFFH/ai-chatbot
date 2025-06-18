from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)
os.environ["TRANSFORMERS_NO_TF"] = "1"  # Don't use TensorFlow
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Disable GPU

# Load a lightweight model using only CPU
chatbot = pipeline("text2text-generation", model="google/flan-t5-small")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Please say something!"})
    result = chatbot(user_input, max_length=100)[0]['generated_text']
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(debug=True)
