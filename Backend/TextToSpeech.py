import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load voice settings from .env
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-US-GuyNeural")

# Path for the MP3 file
AUDIO_PATH = r"Data/speech.mp3"

# Async function to convert text to audio and save it
async def TextToAudioFile(text) -> None:
    if os.path.exists(AUDIO_PATH):
        os.remove(AUDIO_PATH)

    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+10%')
    await communicate.save(AUDIO_PATH)

# Function to play the MP3 file using pygame
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            asyncio.run(TextToAudioFile(Text))

            pygame.mixer.init()
            pygame.mixer.music.load(AUDIO_PATH)
            pygame.mixer.music.play()

            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                if not func():
                    break
                clock.tick(10)
            return True

        except Exception as e:
            print(f"Error in TTS: {e}")

        finally:
            try:
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error in finally block: {e}")

# Function to split long texts and respond smartly
def TextToSpeech(Text, func=lambda r=None: True):
    sentences = str(Text).split(".")

    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(sentences) > 4 and len(Text) >= 250:
        summary = ". ".join(sentences[:2]) + ". " + random.choice(responses)
        TTS(summary, func)
    else:
          TTS(Text, func)

# Run as standalone for testing
if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the text: "))