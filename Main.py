from Frontend.GUI import (
    GraphicalUserInterface,
    SetAsssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus,
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

DefaultMessage = f''' {Username}: Hello {Assistantname}, How are you?
{Assistantname}: Welcome {Username}. I am doing well. How may I help you? '''

functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]
subprocess_list = []



# Ensure a default chat log exists if no chats are logged
def ShowDefaultChatIfNoChats():
    file=open(r'Data\ChatLog.json',"r",encoding='utf-8')
    if len(file.read())<5:
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
                    file.write("")
                with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
                    file.write(DefaultMessage)
    
        
def ReadChatLogjson():
        with open(r'Data\ChatLog.json', "w", encoding='utf-8') as file:
            chatlog_data=json.load(file)
        return chatlog_data
        
    

# Read chat log from JSON
def ReadChatLogJson():
    with open(r'Data\ChatLog.json','r', encoding='utf-8')as file:
        chatlog_data=json.load(file)
    return chatlog_data    

# Integrate chat logs into a readable format


def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"
        formatted_chatlog=formatted_chatlog.replace("User",Username + " ")
        formatted_chatlog=formatted_chatlog.replace("Assistant",Assistantname + " ")    

    # Ensure the Temp directory exists
   

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

# Display the chat on the GUI
def ShowChatOnGUI():
    with open(TempDirectoryPath('Database.data'), 'r', encoding='utf-8') as file:
        data = file.read()
        
    if len(str(data)) > 0:
        lines = data.split('\n')
        result = '\n'.join(lines)
        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
            file.write(result)

            file.close()

    
       

# Initial execution setup
def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatOnGUI()

InitialExecution()
# Main execution logic
def MainExecution():
        TaskExecution = False
        ImageExecution = False
        ImageGenerationQuery = ""

        SetAsssistantStatus("Listening...")
        Query = SpeechRecognition()
        ShowTextToScreen(f"{Username}: {Query}")
        SetAsssistantStatus("Thinking...")
        Decision = FirstLayerDMM(Query)
     
        print("")
        print(f"\nDecision: {Decision}\n")

        G = any([i for i in Decision if i.startswith("general")])
        R = any([i for i in Decision if i.startswith("realtime")])


        Merged_query = " and ".join(
            [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
        )

        for queries in Decision:
            if "generate" in queries:
                ImageGenerationQuery = str(queries)
                ImageExecution = True

        for queries in Decision:
            if not TaskExecution:
                if any(queries.startswith(func) for func in functions):
                    run(Automation(list(Decision)))
                    TaskExecution = True

        if ImageExecution==True:
            with open(r'Frontend\Files\ImageGeneration.data', "w") as file:
                file.write(f"{ImageGenerationQuery},True")

            try:
                p1 = subprocess.Popen(
                    ['python', r"Backend\ImageGeneration.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    shell=False,
                )
                subprocess_list.append(p1)
            except Exception as e:
                print(f"Error starting ImageGeneration.py: {e}")

        if G and R or R:
            SetAsssistantStatus("Searching...")
            Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
            ShowTextToScreen(f"{Assistantname}: {Answer}")
            SetAsssistantStatus("Answering...")
            TextToSpeech(Answer)
            return True
        else:
            for queries in Decision:
                if "general" in queries:
                    SetAsssistantStatus("Thinking...")
                    QueryFinal = queries.replace("general", "")
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                    SetAsssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    return True
                elif "realtime" in queries:
                    SetAsssistantStatus("Searching...")
                    QueryFinal = queries.replace("realtime", "")
                    Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                    SetAsssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    return True
                elif "exit" in queries:
                    QueryFinal = "Okay, Bye!"
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                    SetAsssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    os._exit(1)
  

# Thread for primary execution loop
def FirstThread():
    while True:
        try:
            CurrentStatus = GetMicrophoneStatus()
            print(f"Current Microphone Status: {CurrentStatus}")  # Debugging

            if CurrentStatus.lower() == "true":  # Case-insensitive comparison
                print("Executing MainExecution")  # Debugging
                MainExecution()
            elif CurrentStatus.lower() == "false":
                AIStatus = GetAssistantStatus()
                print(f"Current Assistant Status: {AIStatus}")  # Debugging

                if "Available..." in AIStatus:
                    sleep(0.1)
                else:
                    print("Setting Assistant Status to 'Available...'")  # Debugging
                    SetAsssistantStatus("Available...")
            else:
                print("Unexpected Microphone Status value. Defaulting to 'False'.")  # Debugging
        except Exception as e:
            print(f"Error in FirstThread: {e}")
            sleep(1)  # Avoid infinite rapid errors



# Thread for GUI execution
def SecondThread():
    try:
        GraphicalUserInterface()
    except Exception as e:
        print(f"Error in SecondThread: {e}")

# Entry point
if __name__ == "__main__":
    InitialExecution()
   
    thread1 = threading.Thread(target=FirstThread, daemon=True)
    thread1.start()
    SecondThread()
    