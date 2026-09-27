"""J.A.R.V.I.S. Configuration"""
import os

# LLM Settings (Ollama)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 1024

# Speech Recognition Settings
WAKE_WORD = "jarvis"
LISTEN_TIMEOUT = 5
PHRASE_LIMIT = 10

# TTS Settings
TTS_RATE = 175
TTS_VOLUME = 0.9
TTS_VOICE_INDEX = 0

# Assistant Identity
ASSISTANT_NAME = "J.A.R.V.I.S."
ASSISTANT_VERSION = "1.0.0"
ASSISTANT_PERSONA = (
    "You are J.A.R.V.I.S., an advanced AI assistant inspired by the AI from Iron Man. "
    "You are polite, witty, slightly formal, and always helpful. "
    "Address the user as 'sir' occasionally. "
    "Keep responses concise but informative. "
    "You have a dry British humor and occasional dry wit."
)

# Feature Toggles
ENABLE_WEB_SEARCH = True
ENABLE_SYSTEM_CONTROL = True
ENABLE_REMINDERS = True
ENABLE_WEATHER = True
ENABLE_MUSIC = True

# Paths
REMINDERS_FILE = os.path.join(os.path.dirname(__file__), "reminders.json")
