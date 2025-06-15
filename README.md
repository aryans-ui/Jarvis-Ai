![Jarvis Banner](./Frontend/Graphics/Jarvis-Banner.png)

# 🧠 Jarvis – AI Desktop Assistant

Jarvis is a modular desktop-based AI assistant built with Python, combining Artificial Intelligence (AI), Machine Learning (ML), and speech technology. It interacts with users via voice commands and performs tasks like answering questions, real-time searching, automation, content generation, and much more — just like your own personal assistant!

---

## ✨ Features

- 🎙️ **Speech Recognition & TTS**: Interact with voice using `SpeechRecognition` and `edge-tts`
- 🧠 **LLM Chatbot (Groq)**: Understands and responds to general queries
- 🌍 **Real-time Info Fetching**: Get live news, trends, and updates
- 📂 **App Automation**: Open/close apps, write content, search online, etc.
- 🎨 **AI Image Generation**: Generate images based on prompts using Hugging Face
- 📢 **System Control**: Adjust volume, mute/unmute system, etc.
- 🖥️ **Custom GUI**: Built with Pygame for an interactive desktop interface
- 🧩 **Intent Detection Engine**: Classifies input into general, real-time, system, search, automation, or generation tasks

---

## 🔧 Technologies Used

- **Language**: Python 3
- **Frontend**: Pygame
- **Backend Libraries**:
  - `SpeechRecognition`
  - `edge-tts`
  - `pygame`
  - `selenium`
  - `groq`, `cohere`
  - `huggingface_hub`
  - `openai`, `requests`
- **Architecture**:
  - Modular structure (separate `Backend`, `Frontend`, and `Data`)
  - Intent-based query classification
- **Others**: `.env` config handling, GitHub version control, virtual environments

---

## 📁 Folder Structure
Project Ai/
│
├── Backend/ # All backend logic: AI, automation, TTS, STT, search
├── Frontend/ # Pygame GUI and visual components
│ ├── Files/ # Status, responses, mic, etc.
│ └── Graphics/ # PNGs, GIFs used in UI
├── Data/ # Stores logs, generated images, audio
├── Main.py # Entry point to launch Jarvis
├── .env # API keys and environment variables
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## 🚀 Project Setup Guide 

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/aryans-ui/Jarvis-Ai.git
   cd Jarvis-Ai
2.python -m venv .venv
.venv\Scripts\activate  # For Windows

3. pip install -r requirements.txt
   
4.Set Up .env File (Example):

GROQ_API_KEY=your_key
COHERE_API_KEY=your_key
HUGGINGFACE_API_TOKEN=your_key

5.python --  Main.py


   
