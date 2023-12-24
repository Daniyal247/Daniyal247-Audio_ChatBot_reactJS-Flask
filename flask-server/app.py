from flask import Flask, request, jsonify, send_file
import speech_recognition as sr
import openai
import pyttsx3
import os
import sys
import constants
from flask_cors import CORS, cross_origin
from speech_recognition import AudioData
import whisper
import numpy as np
from scipy.io import wavfile
import soundfile as sf
from pydub import AudioSegment
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={"/upload_audio/allow-cors/*": {"origins": "http://localhost:3000"}})#, resources={r"/upload_audio": {"origins": "http://localhost:3000/upload_audio"}})

openai.api_key = constants.APIKEY
# Path to the audio file where you want to save the recorded user audio
USER_AUDIO_FILE = "user_audio.mp3"
CHATGPT_AUDIO_FILE = "chatgpt_audio.mp3"

@app.route('/upload_audio/allow-cors/', methods=['POST'])
@cross_origin()
def upload_audio():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    if file== '':
        return 'No selected file', 400
    #file_Name = secure_filename(file)
    file_path = os.path.join('input_recording', USER_AUDIO_FILE)
    print(file_path)
    
    file.save(file_path)
    print("file saved")
    #audio_file= open("input_recording/user1_audio.mp3", "rb")

    try:
        audio_file_path = os.path.join('input_recording', USER_AUDIO_FILE)
        audio_file= open(audio_file_path, "rb")
        sys.tracebacklimit = 0  # Remove traceback from Exception
        transcript = openai.Audio.translate("whisper-1", audio_file, file_format="mp3")
        print(transcript['text'])
        print("File path:", audio_file_path)
        if os.path.exists(audio_file_path):
            print("File exists")
            audio_file = open(audio_file_path, "rb")
        else:
            print("File does not exist")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return 'Internal Server Error', 500
    
    chatgpt_reply = say(transcript['text'])
    # chatgpt_audio_file = os.path.join('output_audio', CHATGPT_AUDIO_FILE)
    # print("ef"+chatgpt_audio_file)
    # TTS(chatgpt_reply, chatgpt_audio_file)
    print("response Send")
    return jsonify({"data":chatgpt_reply})

def say(question):
    openai.api_key = constants.APIKEY
    messages = [{"role": "system", "content": "You are a Customer Sales Representative At Neura Sphere AI. You have to sell our services of Chatbots, You have to keep your reply short and humanly"}]
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
    app.run(debug=True, host='127.0.0.1', port=5000)