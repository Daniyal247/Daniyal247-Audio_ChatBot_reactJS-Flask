from flask import Flask, request, jsonify, send_file
import speech_recognition as sr
import openai
import pyttsx3
import os
import constants
from flask_cors import CORS, cross_origin
from speech_recognition import AudioData
import whisper
import numpy as np
from scipy.io import wavfile
import soundfile as sf
from pydub import AudioSegment

app = Flask(__name__)
CORS(app, resources={r"/upload_audio": {"origins": "http://localhost:3000/upload_audio"}})

openai.api_key = constants.APIKEY
# Path to the audio file where you want to save the recorded user audio
USER_AUDIO_FILE = "user_audio.mp3"
CHATGPT_AUDIO_FILE = "chatgpt_audio.mp3"

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file_path = os.path.join('input_recording', USER_AUDIO_FILE)
    print(file_path)
    
    file.save(file_path)
    print("file saved")
    
    
    audio_file= open("input_recording/user_audio.mp3", "rb")
    transcript = openai.Audio.translate("whisper-1", audio_file)
    print(transcript['text'])
    
    chatgpt_reply = say(transcript['text'])
    chatgpt_audio_file = os.path.join('output_audio', CHATGPT_AUDIO_FILE)
    TTS(chatgpt_reply, chatgpt_audio_file)
    #return jsonify({"chatgpt_audio": chatgpt_audio_file})

    # Send the audio file as a response
    return send_file(chatgpt_audio_file, as_attachment=True)

# @app.route("/upload_audio", methods=["POST"])
# @cross_origin()
# def testpost():
#     return send_file("audio.mp3", mimetype="audio/mp3")
@cross_origin()
def testpost():
    return send_file("chatgpt_audio.mp3", mimetype="audio/mp3")


def say(question):
    openai.api_key = constants.APIKEY
    messages = [{"role": "system", "content": "You are a Customer Sales Representative At Neura Sphere AI. You have to sell our services of Chatbots"}]
    if question:
        messages.append({"role": "user", "content": question})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": ChatGPT_reply})
        return ChatGPT_reply

def TTS(answer, output_file):
    engine = pyttsx3.init()
    engine.save_to_file(answer, output_file)
    engine.runAndWait()

if __name__ == "__main__":
    os.makedirs('input_recording', exist_ok=True)
    os.makedirs('output_audio', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
