import requests
import json
import speech_recognition as sr
import pyttsx3

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for your question...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing speech...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Sorry, the speech recognition service is not available."

def get_llama_response(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "prompt": prompt
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return json.loads(response.text)["response"]
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    prompt = recognize_speech_from_mic()
    if prompt.startswith("Sorry"):
        print(prompt)
    else:
        print(f"You said: {prompt}")
        response = get_llama_response(prompt)
        print(f"LLaMA response: {response}")
        speak_text(response)
