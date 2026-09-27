import pyaudio

p = pyaudio.PyAudio()
print("Microphones found:")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info["maxInputChannels"] > 0:
        print(f"  [{i}] {info['name']}")
p.terminate()
