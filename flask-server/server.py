from flask import Flask, request            #added reuest by dani
import speech_recognition as sr
import openai
import constants
import pyttsx3
from pdf_reader import extract_file
#added library by dani
import os

app = Flask(__name__)

#--------------adding new code to get the recording from the front end (by dani)-----------------
# @app.route("/upload_audio", methods=["POST"])
# def upload_audio():
#     try:
#         audio_data = request.files['audio'].read()
#         print(audio_data)
#         # Save the audio data to a file or process it as needed
#         # You can save the audio data to a file or process it using a speech recognition library
#         # For example, you can use the 'speech_recognition' library to convert the audio to text.
#         # Be sure to handle exceptions and errors appropriately.
#         return "Audio received and processed successfully."
#     except Exception as e:
#         return str(e), 500

#-------------------------------------------------------------------------------------------------


#@app.route("/")
#def App():
#    return "Hello World"

def ask():
    UserVoiceRecognizer = sr.Recognizer()

    # Maximum silence duration (in seconds) before stopping recording
    max_silence_duration = 2.0  # Adjust as needed

    while True:
        try:
            with sr.Microphone() as UserVoiceInputSource:
                UserVoiceRecognizer.adjust_for_ambient_noise(UserVoiceInputSource, duration=0.5)

                # The Program listens to the user voice input.
                UserVoiceInput = UserVoiceRecognizer.listen(UserVoiceInputSource, timeout=max_silence_duration)
                
                if UserVoiceInput is None:
                    print("Silence detected. Stopping recording.")
                    break  # Exit the loop if silence is detected

                UserVoiceInput_converted_to_Text = UserVoiceRecognizer.recognize_google(UserVoiceInput)
                UserVoiceInput_converted_to_Text = UserVoiceInput_converted_to_Text.lower()
                print(UserVoiceInput_converted_to_Text)
                user_input = UserVoiceInput_converted_to_Text
                return user_input

        except KeyboardInterrupt:
            print('A KeyboardInterrupt encountered; Terminating the Program !!!')
            exit(0)
        
        except sr.WaitTimeoutError:
            print("Silence detected for too long. Stopping recording.")
            break  # Exit the loop if silence persists for too long

openai.api_key = constants.APIKEY

# Initialize messages with the system message
def Say(question):
    messages = [{"role": "system", "content": extract_file()}]
    
    if question:
        messages.append({"role": "user", "content": question})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": ChatGPT_reply})
        
        return ChatGPT_reply

def tts(answer):
    engine = pyttsx3.init()
    engine.say(answer)
    engine.runAndWait()

tts((Say(ask())))

if __name__ == "__main__":
    app.run(debug=True)