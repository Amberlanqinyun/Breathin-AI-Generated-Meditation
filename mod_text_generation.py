import openai
import os
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def generate_meditation_text(user_input):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the appropriate model
        messages=[
            {"role": "system", "content": "You are a meditation guide."},
            {"role": "user", "content": f"Create a 5-minute guided meditation based on the following thoughts: {user_input}"}
        ],
        max_tokens=500,
        temperature=0.7
    )

    meditation_text = response['choices'][0]['message']['content'].strip()
    return meditation_text

