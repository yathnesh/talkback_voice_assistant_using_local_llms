import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import json
import musicLibrary
import subprocess

recogniser = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def start_ollama():
    try:
        # Start Ollama in a new process
        subprocess.Popen(["ollama", "start"], shell=True)
        print("Ollama server started.")
    except Exception as e:
        print(f"Failed to start Ollama: {e}")

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

def processCommand(c):
    if 'open youtube' in c.lower():
        webbrowser.open("https://youtube.com")
    elif 'open google' in c.lower():
        webbrowser.open("https://google.com")
    elif 'open facebook' in c.lower():
        webbrowser.open("https://facebook.com")
    elif 'open college' in c.lower():
        webbrowser.open("https://vtop.vitap.ac.in/")
    elif 'open gmail' in c.lower():
        webbrowser.open("https://mail.google.com")
    elif 'open instagram' in c.lower():
        webbrowser.open("https://instagram.com")
    elif 'open twitter' in c.lower():
        webbrowser.open("https://twitter.com")
    elif 'open whatsapp' in c.lower():
        webbrowser.open("https://web.whatsapp.com")
    elif 'open amazon' in c.lower():
        webbrowser.open("https://amazon.com")
    elif 'open flipkart' in c.lower():
        webbrowser.open("https://flipkart.com")
    elif 'open netflix' in c.lower():
        webbrowser.open("https://netflix.com")
    elif 'open github' in c.lower():
        webbrowser.open("https://github.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "information" in c.lower():
        r = requests.get("https://newsapi.org/v2/everything?q=tesla&from=2024-09-27&sortBy=publishedAt&apiKey=7fed259939094cb0b544774f6282e989")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                print(article.get('title'))
                speak(article['title'])
    else:
        response = get_llama_response(c)
        print(response)
        speak(response)

if __name__ == "__main__":
    start_ollama()
    speak("Initialising Jarvis.....")
    while True:
        r = sr.Recognizer()
        print("Say Jarvis..")
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            print(word)
            if word.lower() == "jarvis":
                speak("Greetings Sir. How may I help you today.")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    print(audio)
                    command = r.recognize_google(audio)
                    print("input:")
                    print(command)
                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))
#ollama start
#$response = Invoke-WebRequest -Uri "http://localhost:11434/api/generate" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"model": "mistral", "stream": false, "prompt": "Hello"}'

# Display the response content
# $response.Content

