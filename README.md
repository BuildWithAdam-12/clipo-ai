# J.A.R.V.I.S. - Just A Rather Very Intelligent System

An AI voice assistant inspired by Tony Stark's JARVIS from Iron Man, powered by a local LLM via Ollama.

## Features

- **Voice Activation**: Say "Jarvis" to activate, then speak your command
- **AI Conversations**: Powered by local LLM (Ollama) - no API keys needed
- **System Control**: Open apps, shutdown, restart, lock screen
- **Web Search**: Search Google by voice
- **Weather**: Get current weather for any city
- **Reminders**: Set, list, and clear reminders
- **Jokes**: Ask for a joke anytime
- **Time & Date**: Ask what time or date it is
- **Text Mode**: Run without microphone for testing

## Prerequisites

1. **Python 3.8+**
2. **Ollama** - Download from [ollama.com](https://ollama.com)
3. **Microphone** - Required for voice commands

## Setup

### 1. Install Ollama and pull a model

```bash
# Install Ollama from https://ollama.com, then:
ollama pull llama3.2
```

### 2. Start Ollama server

```bash
ollama serve
```

### 3. Install Python dependencies

```bash
cd jarvis
pip install -r requirements.txt
```

## Usage

### Voice Mode (default)
```bash
python main.py
```
Say **"Jarvis"** to wake him up, then speak your command.

### Text Mode (no microphone needed)
```bash
python main.py --text
```
Type your commands directly.

## Voice Commands

| Command | Action |
|---------|--------|
| "Jarvis" | Wake word - activates listening |
| "What time is it?" | Tells current time |
| "What's today's date?" | Tells current date |
| "Tell me a joke" | Tells a random joke |
| "Open notepad" | Opens Notepad |
| "Open google.com" | Opens website |
| "Search for Python tutorials" | Searches Google |
| "Weather in London" | Gets weather |
| "Set reminder buy milk" | Sets a reminder |
| "Show reminders" | Lists all reminders |
| "System info" | Shows system info |
| "Shutdown" | Shuts down computer |
| "Restart" | Restarts computer |
| "Lock screen" | Locks the screen |
| "Clear history" | Clears AI conversation |
| "Goodbye" | Exits JARVIS |

## Configuration

Edit `config.py` to customize:
- LLM model and settings
- Wake word
- TTS voice and speed
- Feature toggles

## Project Structure

```
jarvis/
  main.py           # Entry point
  assistant.py      # Core assistant logic
  speech_engine.py  # Speech recognition & TTS
  ai_backend.py     # Ollama LLM integration
  commands.py       # System commands & utilities
  config.py         # Configuration
  requirements.txt  # Dependencies
```
