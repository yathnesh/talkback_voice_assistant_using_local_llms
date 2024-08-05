from flask import Flask, request, jsonify, send_from_directory
import speech_recognition as sr
import pyttsx3
import requests
import json
import os

app = Flask(__name__)

recogniser = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_llama_response(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "model": "mistral",
        "stream": False,
        "prompt": prompt
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return json.loads(response.text)["response"]
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route('/process_command', methods=['POST'])
def process_command():
    data = request.json
    command = data.get("command")
    
    if 'open youtube' in command.lower():
        os.system("start https://youtube.com")
    elif 'open google' in command.lower():
        os.system("start https://google.com")
    elif 'open facebook' in command.lower():
        os.system("start https://facebook.com")
    elif 'open college' in command.lower():
        os.system("start https://vtop.vitap.ac.in/")
    elif 'open gmail' in command.lower():
        os.system("start https://mail.google.com")
    elif 'open instagram' in command.lower():
        os.system("start https://instagram.com")
    elif 'open twitter' in command.lower():
        os.system("start https://twitter.com")
    elif 'open whatsapp' in command.lower():
        os.system("start https://web.whatsapp.com")
    elif 'open amazon' in command.lower():
        os.system("start https://amazon.com")
    elif 'open flipkart' in command.lower():
        os.system("start https://flipkart.com")
    elif 'open netflix' in command.lower():
        os.system("start https://netflix.com")
    elif 'open github' in command.lower():
        os.system("start https://github.com")
    else:
        response = get_llama_response(command)
        speak(response)
        return jsonify({"response": response})

    return jsonify({"response": "Opened " + command})

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
