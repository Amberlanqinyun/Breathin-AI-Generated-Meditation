from gtts import gTTS

def synthesize_voice(text, language='en', gender='female', speed=0.75):
    # Generate speech using gTTS
    tts = gTTS(text=text, lang=language, slow=(speed < 1.0))
    output_path = "static/output/voice_output.mp3"
    tts.save(output_path)
    return output_path
