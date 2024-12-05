from flask import Flask, render_template, request, jsonify
from groq import Groq

# Initialize Flask app
app = Flask(__name__)

# Set up the Groq API client with your API key
client = Groq(api_key="")  # Replace with your API key

# Helper Functions
def generate_question(role):
    prompt = (
        f"Generate a concise technical interview question for the job role: {role}. "
        f"The question should have a one-word or one-sentence answer. and je questin not ant additional text except question"
    )
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )
    return response.choices[0].message.content.strip()

def generate_hint(question):
    prompt = (
        f"Provide a short and helpful hint for answering this question:\n\n"
        f"Question: {question}\nHint:"
    )
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )
    return response.choices[0].message.content.strip()

def generate_answer(question):
    prompt = (
        f"Provide the correct answer to the following technical interview question. "
        f"The answer should be concise, in one word or one sentence:\n\n"
        f"Question: {question}\nAnswer:"
    )
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"
    )
    return response.choices[0].message.content.strip()

def is_answer_correct(user_answer, correct_answer):
    # Normalize both user answer and correct answer (lowercase and trimmed)
    user_answer = user_answer.strip().lower()
    correct_answer = correct_answer.strip().lower()
    return user_answer == correct_answer

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/question", methods=["POST"])
def question():
    data = request.json
    role = data.get("role")
    if not role:
        return jsonify({"error": "Role is required"}), 400
    question = generate_question(role)
    return jsonify({"question": question})

@app.route("/api/hint", methods=["POST"])
def hint():
    data = request.json
    question = data.get("question")
    hint = generate_hint(question)
    return jsonify({"hint": hint})

@app.route("/api/answer", methods=["POST"])
def answer():
    data = request.json
    question = data.get("question")
    user_answer = data.get("answer")
    correct_answer = generate_answer(question)
    
    # Check if the answer is correct (case-insensitive and trimmed)
    is_correct = is_answer_correct(user_answer, correct_answer)
    
    if is_correct:
        return jsonify({"correct": True, "answer": correct_answer})
    else:
        return jsonify({"correct": False, "answer": correct_answer})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
