"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System
An AI Voice Assistant inspired by Tony Stark's JARVIS from Iron Man.

Usage:
    python main.py              # Run with wake word mode
    python main.py --text       # Run in text-only mode (no microphone)
    python main.py --mic 1      # Use specific microphone index
    python main.py --list-mics  # List available microphones
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from assistant import JarvisAssistant


BANNER = r"""
     ____   ___   __  __       _       _   _ ___ _____
    |  _ \ / _ \ |  \/  | __ _| |_ ___| | | |_ _|_   _|
    | |_) | | | || |\/| |/ _` | __/ _ \ | | || | | |
    |  __/| |_| || |  | | (_| | || (_) \ \ / /| | | |
    |_|    \___/ |_|  |_|\__,_|\__\___/ \___/|___|_|
       Just A Rather Very Intelligent System
"""


def list_microphones():
    import pyaudio
    p = pyaudio.PyAudio()
    print("\n  Available microphones:\n")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"    Mic [{i}]: {info['name']}")
    p.terminate()
    print("\n  Use: python main.py --mic <number>\n")


def main():
    print(BANNER)

    if "--list-mics" in sys.argv:
        list_microphones()
        return

    mic_index = None
    if "--mic" in sys.argv:
        idx = sys.argv.index("--mic")
        if idx + 1 < len(sys.argv):
            mic_index = int(sys.argv[idx + 1])
            print(f"  Using microphone: {mic_index}\n")

    print("  Initializing J.A.R.V.I.S. ...\n")
    jarvis = JarvisAssistant(mic_index=mic_index)

    if "--text" in sys.argv:
        print("  [TEXT MODE] Type your commands (type 'exit' to quit)\n")
        jarvis.startup_sequence()
        jarvis.running = True
        while jarvis.running:
            try:
                command = input("\n  [You]: ").strip()
                if command:
                    jarvis.process_command(command)
            except (KeyboardInterrupt, EOFError):
                jarvis.speech.speak("Goodbye, sir.")
                break
    else:
        jarvis.run()


if __name__ == "__main__":
    main()
