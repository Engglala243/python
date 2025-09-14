import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import time

# API Key
newsapi = "c4bbafa1f09a496ab833436599f28ec4"
openai_api_key = "<API_KEY>"  # Replace with your API key

# Initialize recognizer & TTS engine
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech and play it."""
    try:
        tts = gTTS(text)
        filename = "temp.mp3"
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove(filename)
    except Exception as e:
        print(f"TTS Error: {e}")

def aiProcess(command):
    """Send command to OpenAI API."""
    try:
        client = OpenAI(api_key=openai_api_key)
        completion = client.chat.completions.create(
            model="gpt-3.5",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Start skilled in general tasks like Alexa. Give short, helpful answers."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"AI Error: {e}")
        return "Sorry, I could not process that."

def processCommand(c):
    """Process voice commands."""
    try:
        c = c.lower()
        if "open google" in c:
            webbrowser.open("https://google.com")
        elif "open facebook" in c:
            webbrowser.open("https://facebook.com")
        elif "open youtube" in c:
            webbrowser.open("https://youtube.com")
        elif "open linkedin" in c:
            webbrowser.open("https://linkedin.com")
        elif c.startswith("play"):
            song = c.split(" ", 1)[1]
            link = musicLibrary.music.get(song)
            if link:
                webbrowser.open(link)
            else:
                speak("Sorry, I couldn't find that song.")
        elif "open news" in c:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                articles = r.json().get('articles', [])
                for i, article in enumerate(articles[:5], start=1):  # Read top 5 only
                    print(f"News {i}: {article['title']}")
                    speak(f"News {i}: {article['title']}")
            else:
                speak("Sorry, I could not fetch the news.")
        else:
            output = aiProcess(c)
            print("AI Response:", output)
            speak(output)
    except Exception as e:
        print(f"Command Processing Error: {e}")
        speak("Something went wrong while processing your command.")

def listen(timeout=3, phrase_limit=5):
    """Listen to microphone and return recognized speech."""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            return recognizer.recognize_google(audio)
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Speech Recognition API Error: {e}")
        return None
    except Exception as e:
        print(f"Listening Error: {e}")
        return None

if __name__ == "__main__":
    speak("Initializing AI assistant...")
    print("Say 'Start' to activate me.")

    while True:
        word = listen(timeout=5, phrase_limit=2)
        if word and word.lower() == "start":
            speak("Yes?")
            command = listen(timeout=5, phrase_limit=7)
            if command:
                print("Command:", command)
                processCommand(command)
            else:
                speak("I didn’t hear any command.")
        time.sleep(0.5)  # Prevents CPU overuse
