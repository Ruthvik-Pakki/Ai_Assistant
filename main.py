import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import win32com.client

chat_history = ""


def speak(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)


def chat(query):
    global chat_history
    print(chat_history)
    openai.api_key = apikey
    chat_history += f"User: {query}\nAI: "

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": query},
            {"role": "assistant", "content": chat_history}
        ],
        temperature=0.7,
        max_tokens=256,
    )

    response_text = response["choices"][0]["message"]["content"]
    speak(response_text)
    chat_history += f"{response_text}\n"
    return response_text

def save_ai_response(prompt):
    openai.api_key = apikey
    response_text = f"Response for Prompt: {prompt}\n*************************\n\n"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=256,
    )

    response_text += response["choices"][0]["message"]["content"]

    if not os.path.exists("OpenAI_Responses"):
        os.mkdir("OpenAI_Responses")

    file_name = f"OpenAI_Responses/response_{random.randint(1, 1_000_000)}.txt"
    with open(file_name, "w") as f:
        f.write(response_text)

#works perfectly
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language="en-IN")
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""


if __name__ == '__main__':
    print('Welcome to AI Assistant, How can I Help you?')
    speak("Welcome to AI Assistant, How can I Help you?")

    while True:
        query = listen_command()
        # works perfectly
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"],
            ["facebook", "https://www.facebook.com"],
            ["twitter", "https://www.twitter.com"],
            ["instagram", "https://www.instagram.com"],
            ["linkedin", "https://www.linkedin.com"],
            ["reddit", "https://www.reddit.com"],
            ["pinterest", "https://www.pinterest.com"],
            ["tumblr", "https://www.tumblr.com"],
            ["amazon", "https://www.amazon.com"],
            ["ebay", "https://www.ebay.com"],
            ["netflix", "https://www.netflix.com"],
            ["github", "https://www.github.com"],
            ["stackoverflow", "https://www.stackoverflow.com"],
            ["quora", "https://www.quora.com"],
            ["medium", "https://www.medium.com"],
            ["bbc", "https://www.bbc.com"],
            ["cnn", "https://www.cnn.com"],
            ["spotify", "https://www.spotify.com"]
        ]

        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]}...")
                webbrowser.open(site[1])

        # works perfectly
        if "open music" in query:
            music_path = r"C:\Users\bthem\Downloads\village-background-music-village-music-no-copyright-203060.mp3"

            os.startfile(music_path)
        # works perfectly
        elif "the time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak(f"The current time is {current_time}.")
        # works perfectly
        elif "quit" in query.lower():
            speak("Goodbye!")
            break
        # works perfectly
        elif "reset chat" in query.lower():
            chat_history = ""
            speak("Chat history has been reset.")

        elif "open notion" in query.lower():
            os.startfile(r"C:\Users\bthem\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Notion.lnk")

        elif "open Chrome" in query.lower():
            os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk")


        elif "using artificial intelligence" in query.lower():
            save_ai_response(prompt=query)

        elif query:
            print("Chatting...")
            chat(query)
