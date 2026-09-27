"""J.A.R.V.I.S. Core Assistant Logic"""
import re
from speech_engine import SpeechEngine
from ai_backend import AIBackend
import commands
from config import WAKE_WORD, ASSISTANT_NAME


class JarvisAssistant:
    def __init__(self, mic_index=None):
        self.speech = SpeechEngine(mic_index=mic_index)
        self.ai = AIBackend()
        self.running = False

    def startup_sequence(self):
        self.speech.speak("Good day, sir. All systems are online.")
        if self.ai.is_available():
            models = self.ai.get_available_models()
            model_info = f"Language model: {self.ai.model}"
            if models:
                model_info += f" ({len(models)} models available)"
            self.speech.speak(model_info)
        else:
            self.speech.speak(
                "Warning: Ollama language model is not reachable. "
                "I will operate with built-in commands only. "
                "Please start Ollama and load a model for full AI capabilities."
            )
        self.speech.speak("J.A.R.V.I.S. is ready. How may I assist you today?")

    def process_command(self, command):
        if not command:
            return

        command = command.lower().strip()

        # --- Built-in Commands ---
        if any(kw in command for kw in ["shutdown", "shut down", "power off"]):
            response = commands.shutdown_system()
            self.speech.speak(response)
            return

        if any(kw in command for kw in ["restart", "reboot"]):
            response = commands.restart_system()
            self.speech.speak(response)
            return

        if "cancel shutdown" in command or "cancel restart" in command:
            response = commands.cancel_shutdown()
            self.speech.speak(response)
            return

        if "lock" in command and "screen" in command:
            response = commands.lock_screen()
            self.speech.speak(response)
            return

        if any(kw in command for kw in ["time", "what time"]):
            response = commands.get_current_time()
            self.speech.speak(response)
            return

        if any(kw in command for kw in ["date", "today", "what day"]):
            response = commands.get_current_date()
            self.speech.speak(response)
            return

        if any(kw in command for kw in ["joke", "funny", "laugh"]):
            response = commands.tell_joke()
            self.speech.speak(response)
            return

        if "system info" in command or "system status" in command:
            response = commands.get_system_info()
            self.speech.speak(response)
            return

        if "weather" in command:
            city = self._extract_city(command)
            response = commands.get_weather(city)
            self.speech.speak(response)
            return

        if any(kw in command for kw in ["search", "google", "look up"]):
            query = self._extract_search_query(command)
            response = commands.web_search(query)
            self.speech.speak(response)
            return

        if any(kw in command for kw in ["open", "launch", "start"]):
            target = self._extract_open_target(command)
            if "." in target or "www" in target:
                response = commands.open_website(target)
            else:
                response = commands.open_application(target)
            self.speech.speak(response)
            return

        if any(kw in command for kw in ["set reminder", "remind me", "remember"]):
            text = self._extract_reminder_text(command)
            response = commands.add_reminder(text)
            self.speech.speak(response)
            return

        if any(kw in command for kw in ["list reminders", "show reminders", "what reminders"]):
            response = commands.list_reminders()
            self.speech.speak(response)
            return

        if any(kw in command for kw in ["clear reminders", "delete reminders"]):
            response = commands.clear_reminders()
            self.speech.speak(response)
            return

        if any(kw in command for kw in ["clear history", "clear conversation", "reset"]):
            self.ai.clear_history()
            self.speech.speak("Conversation history cleared.")
            return

        if any(kw in command for kw in ["exit", "quit", "goodbye", "bye", "sleep"]):
            self.speech.speak("Goodbye, sir. Have a pleasant day.")
            self.running = False
            return

        # --- AI Fallback ---
        if self.ai.is_available():
            response = self.ai.query(command)
            self.speech.speak(response)
        else:
            self.speech.speak(
                "I'm sorry, sir. I can only handle built-in commands right now. "
                "The AI language model is not available."
            )

    def _extract_city(self, command):
        match = re.search(r"weather\s+(?:in|for|at)\s+(.+?)(?:\s*$)", command)
        if match:
            return match.group(1).strip()
        return "your location"

    def _extract_search_query(self, command):
        for kw in ["search for", "google", "look up", "search"]:
            if kw in command:
                idx = command.index(kw) + len(kw)
                query = command[idx:].strip()
                if query:
                    return query
        return command

    def _extract_open_target(self, command):
        for kw in ["open", "launch", "start"]:
            if kw in command:
                idx = command.index(kw) + len(kw)
                target = command[idx:].strip()
                if target:
                    return target
        return ""

    def _extract_reminder_text(self, command):
        for kw in ["set reminder", "remind me to", "remind me", "remember to", "remember"]:
            if kw in command:
                idx = command.index(kw) + len(kw)
                text = command[idx:].strip()
                if text:
                    return text
        return command

    def run(self):
        self.running = True
        self.startup_sequence()

        while self.running:
            try:
                if self.speech.listen_for_wake_word(WAKE_WORD):
                    self.speech.speak("Yes, sir?")
                    command = self.speech.listen_for_command()
                    self.process_command(command)
            except KeyboardInterrupt:
                self.speech.speak("Shutting down. Goodbye, sir.")
                self.running = False
                break
