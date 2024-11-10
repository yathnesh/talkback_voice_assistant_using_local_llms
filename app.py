import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
import time
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyController:
    def __init__(self):
        self.client_id = "81874c8dc01544b2aa40eee5a5d8ff84"
        self.client_secret = "4e8e4e63ed594442af126a7eeefb2e6e"
        self.redirect_uri = "http://localhost:8888/callback"
        self.scope = "user-modify-playback-state user-read-playback-state user-library-read playlist-read-private"
        
        # Initialize Spotify with explicit open_browser=True to ensure it tries to open
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scope,
                open_browser=True  # Explicitly request browser open
            ))
            print("Spotify OAuth Initialized")
        except Exception as e:
            print(f"Error initializing Spotify OAuth: {e}")

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")
        
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.spotify = SpotifyController()
        
        self.msg_queue = queue.Queue()
        self.listening = False
        
        self.setup_gui()
        self.update_gui()
        
    def setup_gui(self):
        """Set up GUI components"""
        # Label to display listening status
        self.status_label = tk.Label(self.root, text="Status: Not Listening", font=("Arial", 14), bg="#1e1e1e", fg="white")
        self.status_label.pack(pady=10)
        
        # Button to toggle listening
        self.listen_button = tk.Button(self.root, text="Start Listening", command=self.toggle_listening, font=("Arial", 12), bg="#555555", fg="white")
        self.listen_button.pack(pady=10)
        
        # Scrolled text box for displaying command history
        self.history_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=20, font=("Arial", 12))
        self.history_box.pack(pady=10)

    def toggle_listening(self):
        """Toggle the listening status"""
        if not self.listening:
            self.listening = True
            self.status_label.config(text="Status: Listening...")
            self.listen_button.config(text="Stop Listening")
            threading.Thread(target=self.listen_for_command).start()
        else:
            self.listening = False
            self.status_label.config(text="Status: Not Listening")
            self.listen_button.config(text="Start Listening")

    def listen_for_command(self):
        """Listen for a voice command and process it"""
        while self.listening:
            with sr.Microphone() as source:
                self.status_label.config(text="Listening... Speak now")
                audio = self.recognizer.listen(source)
                self.status_label.config(text="Processing...")
                
                try:
                    command = self.recognizer.recognize_google(audio)
                    self.log_message(f"Received command: {command}")
                    self.process_command(command)
                except sr.UnknownValueError:
                    self.log_message("Could not understand the command.")
                except sr.RequestError as e:
                    self.log_message(f"Error with the speech recognition service: {e}")

                if not self.listening:
                    break
                time.sleep(1)  # Small delay before next listening round

    def process_command(self, command):
        """Process received voice command"""
        self.log_message(f"Processing command: {command}")
        cmd = command.lower()
        
        if cmd.startswith("play"):
            # Code to play song or playlist
            pass
        elif cmd == "pause":
            # Code to pause music
            pass
        # Add more commands as needed

    def log_message(self, message):
        """Log message in the history box and console"""
        print(message)
        self.history_box.insert(tk.END, message + "\n")
        self.history_box.yview(tk.END)

    def update_gui(self):
        """GUI update loop"""
        try:
            message = self.msg_queue.get_nowait()
            self.log_message(message)
        except queue.Empty:
            pass
        self.root.after(100, self.update_gui)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()
