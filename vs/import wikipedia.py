import wikipedia
import pyttsx3
import difflib
import webbrowser  # Import webbrowser module for Google search
import requests
from bs4 import BeautifulSoup

def search_google(query, speak):
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')
    for i, result in enumerate(search_results[:4]):  # Limiting to the first four results
        speak(result.text)

def find_closest_match(query, suggestions):
    closest_match = difflib.get_close_matches(query, suggestions)
    if closest_match:
        return closest_match[0]
    else:
        return None

def main():
    def speak(text):
        engine = pyttsx3.init()
        female_voice = None
        voices = engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower():
                female_voice = voice.id
                break
        if female_voice:
            engine.setProperty('voice', female_voice)
        else:
            print("Female voice not found. Using default voice.")
        engine.setProperty('rate', 200)  # Adjust speech rate (words per minute)
        engine.setProperty('volume', 0.9)  # Adjust volume (0.0 to 1.0)
        engine.say(text)
        engine.runAndWait()

    while True:
        query = input("Enter your query (or type 'exit' to quit): ").strip().lower()
        if query == 'exit':
            break
        elif 'google' in query:
            search_query = query.replace("google", "").strip()
            search_google(search_query, speak)
        else:
            topic = query
            try:
                summary = wikipedia.summary(topic, sentences=2)  # Extract summary
                speak(summary)
            except wikipedia.exceptions.PageError:
                suggestions = wikipedia.search(topic)
                if suggestions:
                    closest_match = find_closest_match(topic, suggestions)
                    if closest_match:
                        try:
                            summary = wikipedia.summary(closest_match, sentences=2)
                            speak(summary)
                        except wikipedia.exceptions.PageError:
                            speak("Page not found. Please check the spelling or try a different topic.")
                    else:
                        speak("Page not found. Please check the spelling or try a different topic.")
                else:
                    speak("Page not found. Please check the spelling or try a different topic.")

if __name__ == "__main__":
    main()