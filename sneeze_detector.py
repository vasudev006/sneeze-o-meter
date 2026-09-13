import cv2
import sounddevice as sd
import numpy as np
import threading
import time
from datetime import datetime


# =========================
# SETTINGS
# =========================

SAMPLE_RATE = 44100
BLOCK_SIZE = 1024

THRESHOLD = 0.008
SILENCE_TIME = 0.30


# =========================
# VARIABLES
# =========================

sneeze_active = False
sneeze_start = None
last_loud_time = None
peak_rms = 0

detected_sneeze = False


# =========================
# SNEEZE RESULT
# =========================

def calculate_result(duration, peak):

    # Power
    # Our microphone readings can reach around 0.05
    power = (peak / 0.05) * 10
    power = max(0, min(10, power))

    # Accuracy / confidence
    accuracy = 50

    if peak > 0.01:
        accuracy += 20

    if peak > 0.02:
        accuracy += 15

    if duration < 1.5:
        accuracy += 10

    if duration < 0.8:
        accuracy += 5

    accuracy = max(0, min(99.9, accuracy))

    return accuracy, power


# =========================
# AUDIO CALLBACK
# =========================

def audio_callback(indata, frames, time_info, status):

    global sneeze_active
    global sneeze_start
    global last_loud_time
    global peak_rms
    global detected_sneeze

    audio = indata[:, 0]

    rms = np.sqrt(np.mean(audio ** 2))

    current_time = time.time()

    # -------------------------
    # LOUD SOUND STARTED
    # -------------------------

    if rms > THRESHOLD:

        if not sneeze_active:

            sneeze_active = True
            sneeze_start = current_time
            peak_rms = rms

            print("\n🚨 EVENT DETECTED!")

        last_loud_time = current_time

        if rms > peak_rms:
            peak_rms = rms

    # -------------------------
    # EVENT ENDED
    # -------------------------

    elif sneeze_active:

        if current_time - last_loud_time > SILENCE_TIME:

            duration = current_time - sneeze_start

            accuracy, power = calculate_result(
                duration,
                peak_rms
            )

            sneeze_time = datetime.now().strftime(
                "%I:%M:%S %p"
            )

            print("\n")
            print("======================================")
            print("          🤧 SNEEZE DETECTED")
            print("======================================")
            print(f"🎯 Sneeze Accuracy : {accuracy:.1f}%")
            print(f"💥 Sneeze Power    : {power:.1f}/10")
            print(f"🕐 Time            : {sneeze_time}")
            print(f"⏱️ Duration        : {duration:.2f} sec")
            print(f"🔊 Peak Sound      : {peak_rms:.4f}")
            print("======================================")

            detected_sneeze = True

            sneeze_active = False
            sneeze_start = None
            last_loud_time = None
            peak_rms = 0


# =========================
# START MICROPHONE
# =========================

audio_stream = sd.InputStream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    channels=1,
    dtype="float32",
    callback=audio_callback
)

audio_stream.start()


# =========================
# START CAMERA
# =========================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("❌ Camera could not be opened.")

    audio_stream.stop()
    audio_stream.close()

    exit()


# =========================
# START
# =========================

print("======================================")
print("          🤧 SNEEZE MEASURE")
print("======================================")
print("📷 Camera       : READY")
print("🎤 Microphone   : READY")
print()
print("Stand in front of the camera.")
print("Make a sneeze-like sound.")
print("Press Q to quit.")
print("======================================")


# =========================
# CAMERA LOOP
# =========================

while True:

    success, frame = camera.read()

    if not success:
        print("❌ Camera error.")
        break

    # Title
    cv2.putText(
        frame,
        "SNEEZE MEASURE",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Status
    if sneeze_active:

        cv2.putText(
            frame,
            "🤧 SNEEZE DETECTED!",
            (30, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            3
        )

    else:

        cv2.putText(
            frame,
            "Listening...",
            (30, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

    cv2.imshow(
        "Sneeze Measure",
        frame
    )

    # Quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# =========================
# CLEANUP
# =========================

audio_stream.stop()
audio_stream.close()

camera.release()
cv2.destroyAllWindows()

print("\n👋 Sneeze Measure stopped.")