"""Local LLM Backend using Ollama"""
import requests
import json
from config import OLLAMA_BASE_URL, LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS, ASSISTANT_PERSONA


class AIBackend:
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL
        self.model = LLM_MODEL
        self.conversation_history = []
        self.system_prompt = ASSISTANT_PERSONA

    def is_available(self):
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return resp.status_code == 200
        except requests.ConnectionError:
            return False

    def query(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history[-20:])

        try:
            resp = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": LLM_TEMPERATURE,
                        "num_predict": LLM_MAX_TOKENS,
                    },
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            assistant_reply = data["message"]["content"].strip()
            self.conversation_history.append({"role": "assistant", "content": assistant_reply})
            return assistant_reply
        except requests.ConnectionError:
            return "I'm unable to connect to the local language model. Please ensure Ollama is running."
        except requests.Timeout:
            return "The language model took too long to respond. Please try again."
        except Exception as e:
            return f"An error occurred while querying the language model: {str(e)}"

    def clear_history(self):
        self.conversation_history.clear()

    def get_available_models(self):
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return [m["name"] for m in data.get("models", [])]
        except Exception:
            pass
        return []
