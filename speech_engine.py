"""Speech Recognition and Text-to-Speech Engine"""
import speech_recognition as sr
import pyttsx3
from config import TTS_RATE, TTS_VOLUME, TTS_VOICE_INDEX, LISTEN_TIMEOUT, PHRASE_LIMIT


class SpeechEngine:
    def __init__(self, mic_index=None):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        if mic_index is not None:
            self.microphone = sr.Microphone(device_index=mic_index)
        else:
            self.microphone = sr.Microphone()

        self.tts_engine = pyttsx3.init()
        self._configure_tts()
        self._calibrate_microphone()

    def _configure_tts(self):
        voices = self.tts_engine.getProperty("voices")
        if len(voices) > TTS_VOICE_INDEX:
            self.tts_engine.setProperty("voice", voices[TTS_VOICE_INDEX].id)
        self.tts_engine.setProperty("rate", TTS_RATE)
        self.tts_engine.setProperty("volume", TTS_VOLUME)

    def _calibrate_microphone(self):
        print("  Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"  Energy threshold: {self.recognizer.energy_threshold}")

    def speak(self, text):
        print(f"\n  [JARVIS]: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        with self.microphone as source:
            try:
                audio = self.recognizer.listen(source, timeout=LISTEN_TIMEOUT, phrase_time_limit=PHRASE_LIMIT)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"  [You]: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                print(f"  [ERROR] Speech recognition service: {e}")
                return None

    def listen_for_wake_word(self, wake_word):
        with self.microphone as source:
            try:
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=3)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"  [Heard]: {text}")
                return wake_word in text
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                return False
            except sr.RequestError:
                return False

    def listen_for_command(self):
        print("  Speak your command...")
        return self.listen()
