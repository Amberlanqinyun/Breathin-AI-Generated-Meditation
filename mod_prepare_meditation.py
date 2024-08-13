from flask import render_template, request, redirect, url_for
from mod_text_generation import generate_meditation_text
from mod_voice_synthesis import synthesize_voice
from pydub import AudioSegment

def prepare_meditation():
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        # Generate meditation content using OpenAI
        meditation_text = generate_meditation_text(user_input)

        # Synthesize voice with default settings
        voice_file_path = synthesize_voice(meditation_text, language='en', gender='female', speed=0.75)

        # Add background music
        background_music = AudioSegment.from_file("static/music/music_1.wav")
        voice_segment = AudioSegment.from_file(voice_file_path)

        # Combine voice with background music
        combined_audio = background_music.overlay(voice_segment)

        # Export the combined audio
        output_file = "static/output/meditation_output.mp3"
        combined_audio.export(output_file, format="mp3")

        return redirect(url_for('start_meditation', audio_file='output/meditation_output.mp3'))

    return render_template('prepare_meditation.html')
