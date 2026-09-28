# PBL Project - Desktop Voice Assistant

A modular, clean, and scalable Python 3.11+ desktop voice assistant designed for rapid, maintainable feature development.

---

## 📂 Project Architecture & Structure

```
PBL PROJECT/
├── .env.example              # Template environment configuration
├── .gitignore                # Git ignore rules for Python, virtual environments, and secrets
├── requirements.txt          # Minimal project dependencies
├── main.py                   # Main entry point to launch the assistant
├── README.md                 # Project documentation and roadmap
└── src/                      # Source code
    ├── __init__.py           # Package indicator
    ├── config/               # Settings & environment variable configuration
    │   ├── __init__.py
    │   └── settings.py
    ├── core/                 # Central orchestration and assistant lifecycle
    │   ├── __init__.py
    │   └── assistant.py
    ├── speech/               # Voice input and audio output interfaces
    │   ├── __init__.py
    │   ├── recognition.py    # Speech-to-Text (STT) interface
    │   └── tts.py            # Text-to-Speech (TTS) interface
    ├── intents/              # Natural language & command understanding
    │   ├── __init__.py
    │   └── parser.py         # Intent parsing & entity extraction
    ├── skills/               # Action execution handlers
    │   ├── __init__.py
    │   ├── system_actions.py # Computer/OS-level automation
    │   └── browser_actions.py# Browser & web automation
    ├── ui/                   # User interface
    │   ├── __init__.py
    │   └── gui.py            # Desktop GUI placeholder (e.g. Tkinter/CustomTkinter)
    └── utils/                # Cross-cutting utilities
        ├── __init__.py
        ├── logger.py         # Standardized logging setup
        └── helpers.py        # Shared helper functions
```

---

## 🎯 Modular Responsibilities

1. **`src/config/`**: Centralized configuration management using environment variables (`.env`) with sensible defaults.
2. **`src/core/`**: Orchestrates data flow between audio capture, intent parsing, skills execution, and speech synthesis.
3. **`src/speech/`**: Isolates audio input (Microphone/STT) and output (TTS) so engines (e.g., SpeechRecognition, pyttsx3) can be swapped without touching core logic.
4. **`src/intents/`**: Decodes user input text into structured intents and actionable parameters.
5. **`src/skills/`**: Encapsulates specific capabilities, separating OS automation from web browsing.
6. **`src/ui/`**: Keeps GUI logic decoupled from backend assistant processing.
7. **`src/utils/`**: Shared tools such as structured logging and timestamp helpers.

---

## 🚀 Getting Started

### 1. Prerequisites
* **Python 3.11+** installed on your system.

### 2. Environment Setup
Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

### 5. Running the Application
```bash
python main.py
```

---

## 📅 6-Day MVP Roadmap

| Day | Focus Area | Key Deliverables |
| :--- | :--- | :--- |
| **Day 1** | **Foundation & Setup** | Project structure, config loader, logging, entry point *(Completed)* |
| **Day 2** | **Speech Pipeline** | Audio input (STT) & Text-to-Speech (TTS) offline engine integration |
| **Day 3** | **Intent & Command Engine** | Rule-based & regex intent matching, basic conversational responses |
| **Day 4** | **System Automation** | OS-level actions (apps, media controls, file tasks, volume) |
| **Day 5** | **Web & Browser Skills** | Web search, opening sites, weather/news fetching |
| **Day 6** | **UI & MVP Polishing** | Lightweight GUI dashboard, error handling, and end-to-end demo testing |
