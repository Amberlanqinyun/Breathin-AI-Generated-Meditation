import openai
from flask import Flask, request, jsonify
from mod_utilize import app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_meditation_text(user_input):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a supportive therapist. Your goal is to help the user feel better and provide guidance. Be empathetic, understanding, and provide actionable advice."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=500,
        temperature=0.7
    )

    meditation_text = response['choices'][0]['message']['content'].strip()
    return meditation_text

@app.route('/chat', methods=['POST'])
def chat_ai():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response_message = generate_meditation_text(user_message)
        suggestions = [
            "Can meditation help with anxiety and stress?",
            "Are there different types of meditation?",
            "What should I focus on while meditating?"
        ]
        return jsonify({'response': response_message, 'suggestions': suggestions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
