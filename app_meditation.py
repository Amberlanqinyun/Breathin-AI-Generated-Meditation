# ''''''
# #from flask import render_template, request, redirect, url_for, flash, session
# import wave
# import io
# import re
# import base64
# import numpy as np
# import openai
# from mod_voice_synthesis import synthesize_ssml, get_voice_list
# from mod_text_generation import generate_text_v1
# from app import app_meditation  # Import the app from app_init

# languages = {
#     "en-US": "English (US)",
#     "en-GB": "English (GB)",
#     "fr-FR": "French",
#     "es-ES": "Spanish",
#     "it-IT": "Italian",
#     "de-DE": "German",
#     "ru-RU": "Russian",
# }

# best_models = {
#     "MALE": {
#         "en-US": "en-US-Neural2-D",
#         "en-GB": "en-GB-Neural2-D",
#         "fr-FR": "fr-FR-Neural2-D",
#         "ru-RU": "ru-RU-Wavenet-D",
#     },
#     "FEMALE": {
#         "en-US": "en-US-Neural2-C",
#         "en-GB": "en-GB-Neural2-C",
#         "fr-FR": "fr-FR-Neural2-C",
#         "ru-RU": "ru-RU-Wavenet-C",
#     }
# }

# musics = {
#     "No Music": [None, 0],
#     "Deep Sound": ["static/musics/music_1.wav", 0.5],
#     "Water Sound": ["static/musics/music_2.wav", 0.25],
# }

# def get_voices(locale, gender):
#     voices = get_voice_list(locale)
#     if gender:
#         gender_index = 1 + (gender == "FEMALE")
#         voices = [voice for voice in voices if voice.ssml_gender == gender_index]
#     return voices

# def superpose_music(meditation, music_path, mix_ratio=0.5):
#     wav_file1 = wave.open(io.BytesIO(meditation), 'rb')
#     wav_file2 = wave.open(music_path, 'rb')

#     params_1 = wav_file1.getparams()
#     params_2 = wav_file2.getparams()

#     frames1 = wav_file1.readframes(params_1.nframes)
#     frames2 = wav_file2.readframes(params_2.nframes)

#     frames1 = np.frombuffer(frames1, dtype=np.int16)
#     frames2 = np.frombuffer(frames2, dtype=np.int16)[:len(frames1)]

#     frames1 = frames1.astype(np.int32)
#     frames2 = frames2.astype(np.int32)

#     frames = mix_ratio * frames1 + (1 - mix_ratio) * frames2
#     frames = frames.astype(np.int16).tobytes()

#     output_audio_io = io.BytesIO()
#     output_audio_header = wave.open(output_audio_io, 'wb')
#     output_audio_header.setparams(params_1)
#     output_audio_header.writeframes(frames)
#     output_audio_header.close()

#     wav_file1.close()
#     wav_file2.close()

#     return output_audio_io.getvalue()

# def concatenate_audio(audio1, audio2, pause_duration=0):
#     wav_file1 = wave.open(io.BytesIO(audio1), 'rb')
#     wav_file2 = wave.open(io.BytesIO(audio2), 'rb')

#     params = wav_file1.getparams()

#     pause_frames = int(params.framerate * pause_duration)
#     silent_segment = np.zeros((pause_frames, params.sampwidth), dtype=np.uint8)
#     silent_audio_byte_object = silent_segment.tobytes()

#     output_audio_io = io.BytesIO()
#     with wave.open(output_audio_io, 'wb') as output_audio_header:
#         output_audio_header.setparams(params)
#         output_audio_header.writeframes(wav_file1.readframes(params.nframes))
#         output_audio_header.writeframes(silent_audio_byte_object)
#         output_audio_header.writeframes(wav_file2.readframes(params.nframes))

#     return output_audio_io.getvalue()

# def generate_audio(meditation, music, sentence_break_time, speaking_rate, voice_model, locale):
#     full_audio = None
#     meditation = meditation.replace(". <", ".<").replace(". ", f". <break time=\"{sentence_break_time}s\" /> ")
#     try:
#         pattern = r'\[PAUSE=(\d+)\]'
#         split_text = re.split(pattern, meditation)
#         times = [int(x) for x in split_text[1::2]]
#         chunks = split_text[::2]

#         full_audio = synthesize_ssml("<speak>" + chunks[0] + "</speak>", model=voice_model.name, locale=locale, speaking_rate=speaking_rate)
#         for i, (chunk, time) in enumerate(zip(chunks[1:], times)):
#             audio = synthesize_ssml("<speak>" + chunk + "</speak>", model=voice_model.name, locale=locale, speaking_rate=speaking_rate)
#             full_audio = concatenate_audio(full_audio, audio, pause_duration=time)

#         if music[0]:
#             full_audio = superpose_music(full_audio, music[0], music[1])

#     except Exception as e:
#         flash(str(e), 'error')
#     return full_audio

# @app_meditation.route('/me', methods=['GET', 'POST'])
# def me():
#     if request.method == 'POST':
#         gender = request.form.get('gender', 'MALE')  # Default to 'MALE' if gender is not present
#         locale = request.form.get('locale', 'en-US')  # Default to 'en-US' if locale is not present
#         music = request.form.get('music', 'No Music')  # Default to 'No Music' if music is not present
#         text = request.form.get('text', '')  # Default to empty string if text is not present
#         openai_model = request.form.get('openai_model', 'text-davinci-003')  # Default to 'text-davinci-003' if openai_model is not present
#         time = int(request.form.get('time', 0))  # Default to 0 if time is not present
#         max_tokens = int(request.form.get('max_tokens', 2000))  # Default to 2000 if max_tokens is not present
#         sentence_break_time = float(request.form.get('sentence_break_time', 0.5))  # Default to 0.5 if sentence_break_time is not present
#         speaking_rate = float(request.form.get('speaking_rate', 1.0))  # Default to 1.0 if speaking_rate is not present
        
#         voice_models = get_voices(locale, gender)
#         voice_model_name = best_models.get(gender, {}).get(locale, "")
#         voice_model = next((model for model in voice_models if model.name == voice_model_name), voice_models[0])

#         try:
#             meditation = generate_text_v1(text, time=time, max_tokens=max_tokens, model=openai_model, language=languages[locale])
#             voice = generate_audio(meditation, musics[music], sentence_break_time, speaking_rate, voice_model, locale)

#             session['meditation'] = meditation
#             session['voice'] = base64.b64encode(voice).decode('utf-8')

#             return redirect(url_for('result'))

#         except Exception as e:
#             flash('An unexpected error occurred: ' + str(e), 'error')
    
#     return render_template('index.html', languages=languages, musics=musics)

# @app_meditation.route('/result')
# def result():
#     voice = base64.b64decode(session.get('voice', ''))
#     return render_template('result.html', voice=voice)

# ''''''