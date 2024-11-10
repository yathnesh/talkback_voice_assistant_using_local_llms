import tkinter as tk
from tkinter import ttk, messagebox
import math
import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import json
import subprocess
import threading
from PIL import Image, ImageTk
import time
import os

class SettingsManager:
    def __init__(self, default_music_library, default_websites):
        self.settings_file = "jarvis_settings.json"
        self.default_music_library = default_music_library
        self.default_websites = default_websites
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.music_library = settings.get('music_library', {})
                self.websites = settings.get('websites', {})
        else:
            # Initialize with default values
            self.music_library = self.default_music_library.copy()
            self.websites = self.default_websites.copy()
            self.save_settings()

    def save_settings(self):
        settings = {
            'music_library': self.music_library,
            'websites': self.websites
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

class SettingsWindow:
    def __init__(self, parent, settings_manager):
        self.window = tk.Toplevel(parent)
        self.window.title("Jarvis Settings")
        self.window.geometry("800x600")
        self.window.configure(bg='#2b2b2b')
        
        self.settings_manager = settings_manager
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create Music Library tab
        self.music_tab = self.create_tab("Music Library")
        self.create_music_widgets()
        
        # Create Websites tab
        self.websites_tab = self.create_tab("Websites")
        self.create_websites_widgets()
        
        # Apply custom styling
        self.style = ttk.Style()
        self.style.configure('Custom.TEntry', padding=5)
        self.style.configure('Custom.TButton', padding=5)

    def create_tab(self, name):
        tab = tk.Frame(self.notebook, bg='#2b2b2b')
        self.notebook.add(tab, text=name)
        return tab

    def create_music_widgets(self):
        # Music Library List
        list_frame = tk.Frame(self.music_tab, bg='#2b2b2b')
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create Treeview for music library
        self.music_tree = ttk.Treeview(list_frame, columns=('Song', 'URL'), show='headings')
        self.music_tree.heading('Song', text='Song Name')
        self.music_tree.heading('URL', text='URL')
        self.music_tree.pack(fill='both', expand=True, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.music_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.music_tree.configure(yscrollcommand=scrollbar.set)
        
        # Add Entry Fields
        entry_frame = tk.Frame(self.music_tab, bg='#2b2b2b')
        entry_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(entry_frame, text="Song Name:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.song_entry = ttk.Entry(entry_frame, style='Custom.TEntry')
        self.song_entry.pack(side='left', padx=5)
        
        tk.Label(entry_frame, text="URL:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.song_url_entry = ttk.Entry(entry_frame, style='Custom.TEntry', width=50)
        self.song_url_entry.pack(side='left', padx=5)
        
        # Buttons
        button_frame = tk.Frame(self.music_tab, bg='#2b2b2b')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="Add Song", command=self.add_song).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_song).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save Changes", command=self.save_changes).pack(side='left', padx=5)
        
        self.refresh_music_list()

    def create_websites_widgets(self):
        # Websites List
        list_frame = tk.Frame(self.websites_tab, bg='#2b2b2b')
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create Treeview for websites
        self.websites_tree = ttk.Treeview(list_frame, columns=('Name', 'URL'), show='headings')
        self.websites_tree.heading('Name', text='Website Name')
        self.websites_tree.heading('URL', text='URL')
        self.websites_tree.pack(fill='both', expand=True, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.websites_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.websites_tree.configure(yscrollcommand=scrollbar.set)
        
        # Add Entry Fields
        entry_frame = tk.Frame(self.websites_tab, bg='#2b2b2b')
        entry_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(entry_frame, text="Website Name:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.website_entry = ttk.Entry(entry_frame, style='Custom.TEntry')
        self.website_entry.pack(side='left', padx=5)
        
        tk.Label(entry_frame, text="URL:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.website_url_entry = ttk.Entry(entry_frame, style='Custom.TEntry', width=50)
        self.website_url_entry.pack(side='left', padx=5)
        
        # Buttons
        button_frame = tk.Frame(self.websites_tab, bg='#2b2b2b')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="Add Website", command=self.add_website).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_website).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save Changes", command=self.save_changes).pack(side='left', padx=5)
        
        self.refresh_websites_list()

    def refresh_music_list(self):
        self.music_tree.delete(*self.music_tree.get_children())
        for song, url in self.settings_manager.music_library.items():
            self.music_tree.insert('', 'end', values=(song, url))

    def refresh_websites_list(self):
        self.websites_tree.delete(*self.websites_tree.get_children())
        for name, url in self.settings_manager.websites.items():
            self.websites_tree.insert('', 'end', values=(name, url))

    def add_song(self):
        song = self.song_entry.get().strip().lower()
        url = self.song_url_entry.get().strip()
        
        if song and url:
            self.settings_manager.music_library[song] = url
            self.refresh_music_list()
            self.song_entry.delete(0, tk.END)
            self.song_url_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Invalid Input", "Please enter both song name and URL")

    def add_website(self):
        name = self.website_entry.get().strip().lower()
        url = self.website_url_entry.get().strip()
        
        if name and url:
            self.settings_manager.websites[name] = url
            self.refresh_websites_list()
            self.website_entry.delete(0, tk.END)
            self.website_url_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Invalid Input", "Please enter both website name and URL")

    def remove_song(self):
        selected = self.music_tree.selection()
        if selected:
            for item in selected:
                values = self.music_tree.item(item)['values']
                if values and values[0] in self.settings_manager.music_library:
                    del self.settings_manager.music_library[values[0]]
            self.refresh_music_list()

    def remove_website(self):
        selected = self.websites_tree.selection()
        if selected:
            for item in selected:
                values = self.websites_tree.item(item)['values']
                if values and values[0] in self.settings_manager.websites:
                    del self.settings_manager.websites[values[0]]
            self.refresh_websites_list()

    def save_changes(self):
        self.settings_manager.save_settings()
        messagebox.showinfo("Success", "Settings saved successfully!")

class VoiceAssistantGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Jarvis Voice Assistant")
        self.window.geometry("600x400")
        self.window.configure(bg='#2b2b2b')
        
        self.default_music_library = {
            "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
            "despacito": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
            "shape": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
            "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA",
            "closer": "https://www.youtube.com/watch?v=PT2_F-1esPk",
            "memories": "https://www.youtube.com/watch?v=SlPhMPnQ58k",
        }
        
        self.default_websites = {
            'youtube': 'https://youtube.com',
            'google': 'https://google.com',
            'facebook': 'https://facebook.com',
            'college': 'https://vtop.vitap.ac.in/',
            'gmail': 'https://mail.google.com',
            'instagram': 'https://instagram.com',
            'twitter': 'https://twitter.com',
            'whatsapp': 'https://web.whatsapp.com',
            'amazon': 'https://amazon.com',
            'flipkart': 'https://flipkart.com',
            'netflix': 'https://netflix.com',
            'github': 'https://github.com'
        }
        
        self.settings_manager = SettingsManager(
            self.default_music_library,
            self.default_websites
        )
        
        self.settings_button = ttk.Button(
            self.window,
            text="Settings",
            command=self.open_settings
        )
        self.settings_button.pack(anchor='ne', padx=20, pady=10)
        
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        
        self.main_frame = tk.Frame(self.window, bg='#2b2b2b')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.title_label = tk.Label(
            self.main_frame, 
            text="JARVIS", 
            font=("Arial", 24, "bold"),
            fg='white',
            bg='#2b2b2b'
        )
        self.title_label.pack(pady=20)
        
        self.canvas_size = 150
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.canvas_size,
            height=self.canvas_size,
            bg='#2b2b2b',
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        self.mic_radius = 30
        self.wave_radius = self.mic_radius
        self.animation_running = False
        self.draw_microphone()
        
        self.text_display = tk.Text(
            self.main_frame,
            height=8,
            width=50,
            font=("Arial", 12),
            bg='#363636',
            fg='white',
            wrap=tk.WORD
        )
        self.text_display.pack(pady=20)
        
        scrollbar = tk.Scrollbar(self.main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_display.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_display.yview)
        
        self.status_label = tk.Label(
            self.main_frame,
            text="Say 'Jarvis' to start",
            font=("Arial", 12),
            fg='white',
            bg='#2b2b2b'
        )
        self.status_label.pack(pady=10)
        
        self.listening_thread = threading.Thread(target=self.start_listening, daemon=True)
        self.listening_thread.start()

    def open_settings(self):
        settings_window = SettingsWindow(self.window, self.settings_manager)

    def draw_microphone(self):
        self.canvas.delete("all")
        
        center_x = self.canvas_size // 2
        center_y = self.canvas_size // 2
        
        if self.animation_running:
            for i in range(3):
                wave_radius = self.wave_radius + (i * 20)
                if wave_radius <= self.canvas_size // 2:
                    self.canvas.create_oval(
                        center_x - wave_radius,
                        center_y - wave_radius,
                        center_x + wave_radius,
                        center_y + wave_radius,
                        outline='#00a8e8',
                        width=2
                    )

        self.canvas.create_oval(
            center_x - self.mic_radius,
            center_y - self.mic_radius,
            center_x + self.mic_radius,
            center_y + self.mic_radius,
            fill='#00a8e8'
        )
        
        mic_width = self.mic_radius * 0.6
        mic_height = self.mic_radius * 1.2
        self.canvas.create_rectangle(
            center_x - mic_width/2,
            center_y - mic_height/2,
            center_x + mic_width/2,
            center_y + mic_height/2,
            fill='white'
        )

    def animate_microphone(self):
        if self.animation_running:
            self.wave_radius += 2
            if self.wave_radius > self.canvas_size // 2:
                self.wave_radius = self.mic_radius
            
            self.draw_microphone()
            self.window.after(50, self.animate_microphone)

    def update_text_display(self, text, user_message=False):
        if user_message:
            self.text_display.insert(tk.END, f"You: {text}\n")
        else:
         self.text_display.insert(tk.END, f"Jarvis: {text}\n")
        self.text_display.see(tk.END)

    def _update_text_display_safe(self, text, clear):
        if clear:
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, f"{text}\n")
        self.text_display.see(tk.END)

    def speak(self, text):
        self.update_text_display(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def start_ollama(self):
        try:
            subprocess.Popen(["ollama", "start"], shell=True)
            print("Ollama server started.")
        except Exception as e:
            print(f"Failed to start Ollama: {e}")

    def get_llama_response(self, prompt):
        url = "http://localhost:11434/api/generate"
        headers = {'Content-Type': 'application/json'}
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

    def process_command(self, command):
        self.update_text_display(f"You: {command}", user_message=True)
        cmd_lower = command.lower()
        
        websites = {
            'open youtube': 'https://youtube.com',
            'open google': 'https://google.com',
            'open facebook': 'https://facebook.com',
            'open college': 'https://vtop.vitap.ac.in/',
            'open gmail': 'https://mail.google.com',
            'open instagram': 'https://instagram.com',
            'open twitter': 'https://twitter.com',
            'open whatsapp': 'https://web.whatsapp.com',
            'open amazon': 'https://amazon.com',
            'open flipkart': 'https://flipkart.com',
            'open netflix': 'https://netflix.com',
            'open github': 'https://github.com'
        }
        
        for command_text, url in websites.items():
            if command_text in cmd_lower:
                webbrowser.open(url)
                self.speak(f"Opening {command_text.replace('open ', '')}")
                return
        
        if cmd_lower.startswith("play "):
            song = cmd_lower.split("play ")[1].strip()
            if song in self.settings_manager.music_library:
                webbrowser.open(self.settings_manager.music_library[song])
                self.speak(f"Playing {song}")
                return
            else:
                self.speak(f"Sorry, I couldn't find {song} in the music library")
                return
        
        # Replace the if "information" in cmd_lower or "news" in cmd_lower section with this:

        if "information" in cmd_lower or "news" in cmd_lower:
            try:
                self.speak("Fetching the latest news headlines")
                
                # Using GNews API for English news only
                url = "https://gnews.io/api/v4/top-headlines"
                params = {
                    'lang': 'en',
                    'country': 'us',
                    'max': 10,  # Requesting 10 articles
                    'apikey': 'a42e9aabc94d799a8170fdb6b96296e6'  # Replace with your API key
                }
                
                # Make the API request with timeout
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                news_data = response.json()
                
                if 'articles' not in news_data or not news_data['articles']:
                    self.speak("Sorry, I couldn't fetch the news at the moment")
                    return
                    
                articles = news_data['articles'][:10]  # Ensure we only get 10 articles
                
                # Clear previous text and show header
                self.text_display.delete(1.0, tk.END)
                self.text_display.insert(tk.END, "Top 10 News Headlines:\n\n")
                
                # Process each article
                for i, article in enumerate(articles, 1):
                    # Extract title and source, with fallbacks if data is missing
                    title = article.get('title', 'No title available')
                    source = article.get('source', {}).get('name', 'Unknown source')
                    
                    # Format the news item
                    news_item = f"{i}. {title}\n   Source: {source}\n\n"
                    
                    # Update display
                    self.text_display.insert(tk.END, news_item)
                    
                    # Speak the title
                    self.speak(f"News {i}: {title}")
                    
                    # Small delay between articles for better speech clarity
                    time.sleep(0.5)
                    
            except requests.exceptions.RequestException as e:
                print(f"Network error: {e}")
                self.speak("Sorry, I'm having trouble connecting to the news service")
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                self.speak("Sorry, I received an invalid response from the news service")
            except Exception as e:
                print(f"Unexpected error: {type(e).__name__}, {e}")
                self.speak("Sorry, I encountered an error while fetching the news")
            return

        response = self.get_llama_response(command)
        self.speak(response)

    def update_status(self, text):
        self.window.after(0, lambda: self.status_label.config(text=text))

    def start_listening(self):
        self.start_ollama()
        self.speak("Initializing Jarvis.....")
        
        while True:
            try:
                with sr.Microphone() as source:
                    self.update_status("Listening for 'Jarvis'...")
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=1)
                    
                word = self.recognizer.recognize_google(audio)
                self.update_text_display(f"Heard: {word}")
                
                if word.lower() == "jarvis":
                    self.animation_running = True
                    self.animate_microphone()
                    self.speak("Greetings Sir. How may I help you today.")
                    
                    with sr.Microphone() as cmd_source:
                        self.update_status("Listening for command...")
                        command_audio = self.recognizer.listen(cmd_source)
                        command = self.recognizer.recognize_google(command_audio)
                        self.process_command(command)
                    
                    self.animation_running = False
                    self.wave_radius = self.mic_radius
                    self.draw_microphone()
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"Error: {e}")
                continue

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = VoiceAssistantGUI()
    app.run()