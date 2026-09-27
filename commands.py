"""System Commands and Utilities"""
import os
import sys
import subprocess
import json
import time
import webbrowser
import datetime
import random
from config import REMINDERS_FILE


# --- App Launching ---
APP_COMMANDS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "edge": "msedge.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "terminal": "cmd.exe",
    "task manager": "taskmgr.exe",
    "settings": "ms-settings:",
    "control panel": "control.exe",
}


def open_application(app_name):
    app_name = app_name.lower().strip()
    if app_name in APP_COMMANDS:
        try:
            subprocess.Popen(APP_COMMANDS[app_name], shell=True)
            return f"Opening {app_name}."
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"
    return f"I don't know how to open '{app_name}'."


def open_website(url):
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opening {url}"


# --- System Control ---
def get_system_info():
    import platform
    system = platform.system()
    node = platform.node()
    release = platform.release()
    return f"Running on {system} {release}, machine: {node}"


def shutdown_system(delay=5):
    os.system(f"shutdown /s /t {delay}")
    return f"Shutting down in {delay} seconds."


def restart_system(delay=5):
    os.system(f"shutdown /r /t {delay}")
    return f"Restarting in {delay} seconds."


def cancel_shutdown():
    os.system("shutdown /a")
    return "Shutdown cancelled."


def lock_screen():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "Screen locked."


# --- Time & Date ---
def get_current_time():
    return datetime.datetime.now().strftime("It's %I:%M %p.")


def get_current_date():
    return datetime.datetime.now().strftime("Today is %A, %B %d, %Y.")


# --- Jokes ---
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why do Java developers wear glasses? Because they can't C#.",
    "What's a programmer's favorite hangout place? Foo Bar.",
    "Why did the developer go broke? Because he used up all his cache.",
    "A SQL query walks into a bar, sees two tables and asks... Can I join you?",
    "Why do programmers hate nature? It has too many bugs.",
    "What's a computer's favorite snack? Microchips.",
    "How do trees get on the internet? They log in.",
    "Why was the computer cold? It left its Windows open.",
    "What do you call a computer that sings? A-Dell.",
    "Why did the AI break up with the internet? Too many connections.",
    "I told my computer I needed a break. Now it won't stop showing me vacation ads.",
]


def tell_joke():
    return random.choice(JOKES)


# --- Reminders ---
def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    return []


def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)


def add_reminder(text):
    reminders = load_reminders()
    reminders.append({
        "text": text,
        "time": datetime.datetime.now().isoformat(),
        "active": True,
    })
    save_reminders(reminders)
    return f"Reminder set: {text}"


def list_reminders():
    reminders = [r for r in load_reminders() if r.get("active")]
    if not reminders:
        return "You have no active reminders."
    lines = [f"  {i+1}. {r['text']} (since {r['time'][:10]})" for i, r in enumerate(reminders)]
    return "Your reminders:\n" + "\n".join(lines)


def clear_reminders():
    save_reminders([])
    return "All reminders cleared."


# --- Weather (basic, requires internet) ---
def get_weather(city="your location"):
    try:
        import urllib.request
        url = f"https://wttr.in/{city}?format=3"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.read().decode("utf-8").strip()
    except Exception:
        return "Unable to fetch weather data right now."


# --- Web Search ---
def web_search(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching Google for: {query}"
