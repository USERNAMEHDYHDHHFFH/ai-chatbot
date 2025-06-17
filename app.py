from flask import Flask, request, jsonify, render_template
from transformers import pipeline

app = Flask(__name__)

# Use flan-t5-large (better performance, still free)
generator = pipeline("text2text-generation", model="google/flan-t5-base")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "Please say something."})

    # Better prompt formatting
    if any(char in user_input for char in "0123456789*+/-="):
        prompt = f"Solve this: {user_input}"
    else:
        prompt = f"Chat with the user: {user_input}"

    try:
        result = generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
        return jsonify({"reply": result.strip()})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Sorry, something went wrong."})

if __name__ == "__main__":
    app.run(debug=True)
