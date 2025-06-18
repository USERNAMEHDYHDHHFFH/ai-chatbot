from flask import Flask, render_template, request, jsonify
from transformers import pipeline, set_seed

# Load model
generator = pipeline('text-generation', model='gpt2')
set_seed(42)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["message"]
        output = generator(user_input, max_length=100, num_return_sequences=1)
        reply = output[0]["generated_text"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Sorry, something went wrong."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

