import os
from groq import Groq

# Set up the Groq API client with your API key
client = Groq(api_key="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")  # Replace with your Groq API key


def generate_question(role):
    """
    Generate a concise technical question based on the job role using the Groq API.
    """
    prompt = (
        f"Generate a concise technical interview question for the job role: {role}. "
        f"The question should have a one-word or one-sentence answer."
    )
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"  # Replace with the desired Groq model
    )
    return response.choices[0].message.content.strip()


def generate_hint(question):
    """
    Generate a concise hint for the given question using the Groq API.
    """
    prompt = (
        f"Provide a short and helpful hint for answering this question:\n\n"
        f"Question: {question}\nHint:"
    )
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"  # Replace with the desired Groq model
    )
    return response.choices[0].message.content.strip()


def generate_answer(question):
    """
    Generate the correct answer for the given question using the Groq API.
    """
    prompt = (
        f"Provide the correct answer to the following technical interview question. "
        f"The answer should be concise, in one word or one sentence:\n\n"
        f"Question: {question}\nAnswer:"
    )
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192"  # Replace with the desired Groq model
    )
    return response.choices[0].message.content.strip()


def interview_loop(role):
    """
    Main loop for conducting the technical interview with concise Q&A.
    """
    score = 0
    print("\nWelcome to the Technical Interview Simulator!")
    print(f"Role: {role}")
    print("Type 'hint' for a hint (costs 5 points), 'quit' to exit the interview.\n")

    while True:
        # Generate a question
        question = generate_question(role)
        print(f"Question: {question}")
        
        # Get user's answer
        user_input = input("Your Answer: ").strip()

        if user_input.lower() == "quit":
            print(f"Exiting the interview. Your final score is: {score}")
            break
        elif user_input.lower() == "hint":
            # Generate and show a hint, deduct points
            hint = generate_hint(question)
            print(f"Hint: {hint}")
            score -= 5
        else:
            # Check if the answer is correct or incorrect
            correct_answer = generate_answer(question)
            if user_input.lower() == correct_answer.lower():
                print("Correct! You earned 10 points.")
                score += 10
            else:
                print(f"Incorrect. The correct answer is: {correct_answer}.")
                score -= 4

        print(f"Your current score is: {score}\n")


if __name__ == "__main__":
    # Get the job role from the user
    role = input("Enter the job role you're applying for: ").strip()
    interview_loop(role)
