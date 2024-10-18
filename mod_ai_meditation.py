import openai
import os
from dotenv import load_dotenv
import hashlib
from pathlib import Path
from pydub import AudioSegment
from flask import render_template, request, redirect, url_for
from mod_utilize import app
from google.cloud import texttospeech
import logging

# Load environment variables from .env file
load_dotenv()

# Set the path for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Caching function to store and retrieve files
def cache_file(content, file_type):
    content_hash = hashlib.md5(content.encode()).hexdigest()  # Create a unique hash
    cache_dir = Path("static/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)  # Ensure cache directory exists

    # File path is determined by the hash of the input content
    file_path = cache_dir / f"{content_hash}.{file_type}"

    if file_path.exists():
        logging.info(f"Serving cached {file_type} file.")
        return file_path  # Return the cached file if it exists
    else:
        logging.info(f"Generating new {file_type} file.")
        return file_path  # Return the path for a new file to be created

# Generate Meditation Text and Cache it
def generate_meditation_text(user_input):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Check if the text exists in cache
    cached_file = cache_file(user_input, "txt")
    if cached_file.exists():
        with open(cached_file, "r") as f:
            return f.read()

    # Generate meditation text using OpenAI GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a meditation guide."},
            {"role": "user", "content": f"Create a 5-minute guided meditation: {user_input}"}
        ],
        max_tokens=500,
        temperature=0.7
    )

    meditation_text = response['choices'][0]['message']['content'].strip()

    # Save the generated text to cache
    with open(cached_file, "w") as f:
        f.write(meditation_text)

    return meditation_text

# Add SSML tags for pauses after periods and commas
def add_ssml_pauses(text):
    text = text.replace('.', '<break time="5s"/>').replace(',', '<break time="2s"/>')
    ssml_text = f"<speak>{text}</speak>"
    return ssml_text

# Synthesize Voice with Google Cloud TTS using SSML for pauses
def synthesize_voice(meditation_text, voice="en-US-Wavenet-D", language="en", speed=0.65, pitch=-10.0):
    client = texttospeech.TextToSpeechClient()

    # Convert the text to SSML with pauses
    ssml_text = add_ssml_pauses(meditation_text)

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Select the language, voice, and parameters like speaking rate and pitch
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language,
        name=voice,
        ssml_gender=texttospeech.SsmlVoiceGender.MALE  # Deep male voice
    )

    # Set the audio configuration with pitch and speaking rate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,  # Slower rate for calmness
        pitch=pitch  # Lower pitch for deep voice
    )

    # Generate speech
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config
    )

    # Save the response to an MP3 file
    file_path = cache_file(meditation_text, "mp3")
    with open(file_path, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file {file_path}")

    return file_path

# Combine Voice with Background Music
def combine_voice_with_music(voice_file, background_music_file, output_file):
    background_music = AudioSegment.from_file(background_music_file)
    voice_segment = AudioSegment.from_file(voice_file)
    
    # Adjust the volume if necessary (e.g., lowering background music)
    background_music = background_music + 10  # Lower the background music by 10 dB

    # Combine the voice with background music
    combined_audio = background_music.overlay(voice_segment)

    # Export the combined audio to a file
    combined_audio.export(output_file, format="mp3")
    logging.info(f"Combined audio exported successfully: {output_file}")

    return output_file

# Main function to prepare the meditation
def prepare_meditation():
    if request.method == 'POST':
        try:
            # Get user input
            user_input = request.form.get('user_input')
            logging.info(f"User Input: {user_input}")

            # Generate meditation text using OpenAI API
            meditation_text = generate_meditation_text(user_input)
            logging.info(f"Generated Meditation Text: {meditation_text}")

            if not meditation_text:
                raise ValueError("No meditation text generated.")

            # Synthesize voice with Google Cloud TTS
            voice_file_path = synthesize_voice(meditation_text, language='en', speed=0.75, pitch=-5.0)
            logging.info(f"Voice File Path: {voice_file_path}")

            # Ensure the synthesized voice file path is valid
            if not voice_file_path or not os.path.exists(voice_file_path):
                raise FileNotFoundError(f"Voice file not found: {voice_file_path}")

            # Add background music (ensure the music file exists)
            background_music_path = "static/music/music_1.wav"
            if not os.path.exists(background_music_path):
                raise FileNotFoundError(f"Background music file not found: {background_music_path}")

            # Combine the audio files
            output_file = "static/output/meditation_output.mp3"
            combine_voice_with_music(voice_file_path, background_music_path, output_file)

            # Redirect to the meditation playback page
            return redirect(url_for('start_meditation', audio_file='output/meditation_output.mp3'))

        except Exception as e:
            logging.error(f"Error during meditation generation: {e}")
            return render_template('error.html', error=str(e))  # Render an error page or message

    return render_template('meditation_page.html')

# Flask route to start the meditation session
@app.route("/start_meditation")
def start_meditation():
    audio_file = request.args.get('audio_file')
    return render_template('start_meditation.html', audio_file=audio_file)
