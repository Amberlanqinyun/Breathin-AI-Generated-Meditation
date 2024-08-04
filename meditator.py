import wave
import io
import re
import base64
import numpy as np
import streamlit as st
from streamlit.components.v1 import html

from mod_voice_synthesis import synthesize_ssml, get_voice_list
from mod_text_generation import generate_text_v1
from mod_layout_config import set_page_config, apply_custom_css

# Set the page configuration and apply custom CSS
set_page_config()
apply_custom_css()

languages = {
    "en-US": "English (US)",
    "en-GB": "English (GB)",
    "fr-FR": "French",
    "es-ES": "Spanish",
    "it-IT": "Italian",
    "de-DE": "German",
    "ru-RU": "Russian",
}

best_models = {
    "MALE": {
        "en-US": "en-US-Neural2-D",
        "en-GB": "en-GB-Neural2-D",
        "fr-FR": "fr-FR-Neural2-D",
        "ru-RU": "ru-RU-Wavenet-D",
    },
    "FEMALE": {
        "en-US": "en-US-Neural2-C",
        "en-GB": "en-GB-Neural2-C",
        "fr-FR": "fr-FR-Neural2-C",
        "ru-RU": "ru-RU-Wavenet-C",
    }
}

musics = {
    "No Music": [None, 0],
    "Deep Sound": ["musics/music_1.wav", 0.5],
    "Water Sound": ["musics/music_2.wav", 0.25],
}

safari_warning_html = """
<div id="safari-warning" style="display: none;">
<div style="background-color: #ffe3121a; color: #926c05; padding: 10px; border-radius: 5px; font-style: italic; font-family: 'Source Sans Pro'">
    <b>Warning:</b> In Safari, the audio player is sometimes throwing an error, please use another browser or download the meditation.
</div>
</div>
<script>
var isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
if (isSafari) {
document.getElementById("safari-warning").style.display = "block";
}
</script>
"""

@st.cache_data
def get_voices(locale, gender):
    voices = get_voice_list(locale)
    if gender:
        gender_index = 1 + (gender == "FEMALE")
        voices = [voice for voice in voices if voice.ssml_gender == gender_index]
    return voices

def superpose_music(meditation, music_path, mix_ratio=0.5):
    wav_file1 = wave.open(io.BytesIO(meditation), 'rb')
    wav_file2 = wave.open(music_path, 'rb')

    params_1 = wav_file1.getparams()
    params_2 = wav_file2.getparams()

    frames1 = wav_file1.readframes(params_1.nframes)
    frames2 = wav_file2.readframes(params_2.nframes)

    frames1 = np.frombuffer(frames1, dtype=np.int16)
    frames2 = np.frombuffer(frames2, dtype=np.int16)[:len(frames1)]

    frames1 = frames1.astype(np.int32)
    frames2 = frames2.astype(np.int32)

    frames = mix_ratio * frames1 + (1 - mix_ratio) * frames2
    frames = frames.astype(np.int16).tobytes()

    output_audio_io = io.BytesIO()
    output_audio_header = wave.open(output_audio_io, 'wb')
    output_audio_header.setparams(params_1)
    output_audio_header.writeframes(frames)
    output_audio_header.close()

    wav_file1.close()
    wav_file2.close()
    
    return output_audio_io.getvalue()

def concatenate_audio(audio1, audio2, pause_duration=0):
    wav_file1 = wave.open(io.BytesIO(audio1), 'rb')
    wav_file2 = wave.open(io.BytesIO(audio2), 'rb')

    params = wav_file1.getparams()

    pause_frames = int(params.framerate * pause_duration)
    silent_segment = np.zeros((pause_frames, params.sampwidth), dtype=np.uint8)
    silent_audio = silent_segment.tobytes()

    output_audio_io = io.BytesIO()
    with wave.open(output_audio_io, 'wb') as output_audio_header:
        output_audio_header.setparams(params)
        output_audio_header.writeframes(wav_file1.readframes(params.nframes))
        output_audio_header.writeframes(silent_audio)
        output_audio_header.writeframes(wav_file2.readframes(params.nframes))

    wav_file1.close()
    wav_file2.close()

    return output_audio_io.getvalue()
