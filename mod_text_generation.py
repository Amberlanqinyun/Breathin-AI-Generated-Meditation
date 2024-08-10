import openai

def generate_meditation_text(user_input):
    openai.api_key = 'your-openai-api-key'

    prompt = f"Create a 5-minute guided meditation based on the following thoughts: {user_input}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,  # Adjust based on the length of content needed
        n=1,
        stop=None,
        temperature=0.7
    )

    meditation_text = response.choices[0].text.strip()
    return meditation_text
