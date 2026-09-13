import sounddevice as sd
import numpy as np

SAMPLE_RATE = 44100
DURATION = 5

print("🎤 Microphone test starting...")
print("Speak, clap, or make some noise!")

recording = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32"
)

sd.wait()

volume = np.sqrt(np.mean(recording ** 2))

print(f"\n✅ Recording complete!")
print(f"Average microphone level: {volume:.4f}")