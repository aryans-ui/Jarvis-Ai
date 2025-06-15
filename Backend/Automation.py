
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
import platform
import re

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
client = Groq(api_key=GroqAPIKey)

SystemChatBot = [{
    "role": "system",
    "content": f"Hello, I am {os.environ.get('Username', 'User')}, a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems, etc."
}]
messages = []

def GoogleSearch(topic):
    search(topic)
    return True

def Content(topic):
    def OpenNotepad(File):
        subprocess.Popen(['notepad.exe', File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": prompt})
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  

            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True
        )
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})
        return answer

    topic = topic.replace("content", "").strip()
    path = rf"Data\{topic.lower().replace(' ', '_')}.txt"
    os.makedirs("Data", exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(ContentWriterAI(topic))
    OpenNotepad(path)
    return True

def YouTubeSearch(topic):
    url = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(url)
    return True

def PlayYoutube(query):
    try:
        playonyt(query)
        return True
    except Exception as e:
        print(f"Error playing YouTube video: {e}")
        return False

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f"https://www.microsoft.com/en-us/search?q={query}"
            headers = {"User-Agent": "Mozilla/5.0"}
            res = sess.get(url, headers=headers)
            return res.text if res.status_code == 200 else None

        def open_in_chrome_beta(url):
            try:
                paths = [
                    r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome Beta\Application\chrome.exe",
                    os.path.expanduser(r"~\AppData\Local\Google\Chrome Beta\Application\chrome.exe")
                ]
                for path in paths:
                    if os.path.exists(path):
                        subprocess.run([path, url])
                        return True
                webbrowser.open(url)
                return True
            except Exception as e:
                print(f"Error: {e}")
                webbrowser.open(url)
                return True

        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                open_in_chrome_beta(links[0])
        return True

def CloseApp(app):
    if "chrome" in app.lower():
        subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], check=True)
        return True
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"Error closing {app}: {e}")
        return False

def System(command):
    actions = {
        "mute": lambda: keyboard.press_and_release("volume mute"),
        "unmute": lambda: keyboard.press_and_release("volume mute"),
        "volume up": lambda: keyboard.press_and_release("volume up"),
        "volume down": lambda: keyboard.press_and_release("volume down")
    }
    func = actions.get(command)
    if func:
        func()
        return True
    print(f"Unknown system command: {command}")
    return False

def clean_input_commands(commands):
    return [
        re.sub(r'^[\*\-\d\.\)]*\s*["“”]?(.+?)["“”]?\s*$', r'\1', cmd.strip())
        for cmd in commands
    ]

async def TranslateAndExecute(commands):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            funcs.append(asyncio.to_thread(OpenApp, command[5:].strip()))
        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command[6:].strip()))
        elif command.startswith("play "):
            funcs.append(asyncio.to_thread(PlayYoutube, command[5:].strip()))
        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(Content, command[8:].strip()))
        elif command.startswith("google search "):
            funcs.append(asyncio.to_thread(GoogleSearch, command[14:].strip()))
        elif command.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YouTubeSearch, command[15:].strip()))
        elif command.startswith("system "):
            funcs.append(asyncio.to_thread(System, command[7:].strip()))
        else:
            print(f"No function found for command: {command}")

    if funcs:
        results = await asyncio.gather(*funcs, return_exceptions=True)
        for i, result in enumerate(results):
            print(f"Command {i+1} result: {result}")
    else:
        print("No valid commands to execute")

async def Automation(commands):
    commands = clean_input_commands(commands)
    print(f"Starting automation with commands: {commands}")
    await TranslateAndExecute(commands)

if __name__ == "__main__":
    test_commands = [
        "close notepad",
        "content application for sick leave",
        "open Settings",
        "play vishnu strotam  song on youtube"
    ]
    asyncio.run(Automation(test_commands))
