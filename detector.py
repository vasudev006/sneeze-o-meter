import sounddevice as sd
import numpy as np
import time
from datetime import datetime


# =========================
# AUDIO SETTINGS
# =========================

SAMPLE_RATE = 44100
BLOCK_SIZE = 512

THRESHOLD = 0.008
SILENCE_TIME = 0.15


# =========================
# CALCULATE RESULT
# =========================

def calculate_result(duration, peak_rms):

    # -------------------------
    # SNEEZE POWER
    # -------------------------

    power = (peak_rms / 0.05) * 10

    power = max(
        0,
        min(10, power)
    )


    # -------------------------
    # SNEEZE ACCURACY
    # -------------------------

    accuracy = 50

    if peak_rms > 0.01:
        accuracy += 20

    if peak_rms > 0.02:
        accuracy += 15

    if duration < 1.5:
        accuracy += 10

    if duration < 0.8:
        accuracy += 5

    accuracy = min(
        99.9,
        accuracy
    )


    return accuracy, power


# =========================
# DETECT SNEEZE
# =========================

def detect_sneeze():

    sneeze_active = False

    sneeze_start = None

    last_loud_time = None

    peak_rms = 0

    result = None


    # =========================
    # MICROPHONE CALLBACK
    # =========================

    def audio_callback(
        indata,
        frames,
        time_info,
        status
    ):

        nonlocal sneeze_active
        nonlocal sneeze_start
        nonlocal last_loud_time
        nonlocal peak_rms
        nonlocal result


        # Get microphone audio

        audio = indata[:, 0]


        # Calculate RMS volume

        rms = np.sqrt(
            np.mean(
                audio ** 2
            )
        )


        current_time = time.time()


        # =========================
        # LOUD SOUND DETECTED
        # =========================

        if rms > THRESHOLD:

            # Start new sneeze event

            if not sneeze_active:

                sneeze_active = True

                sneeze_start = current_time

                peak_rms = rms


            # Update last loud time

            last_loud_time = current_time


            # Save loudest RMS

            peak_rms = max(
                peak_rms,
                rms
            )


        # =========================
        # SOUND BECAME QUIET
        # =========================

        elif sneeze_active:

            if (
                current_time
                - last_loud_time
                > SILENCE_TIME
            ):

                # Calculate duration

                duration = (
                    current_time
                    - sneeze_start
                )


                # Calculate scores

                accuracy, power = calculate_result(
                    duration,
                    peak_rms
                )


                # =========================
                # FINAL RESULT
                # =========================

                result = {

                    "accuracy":
                        float(
                            round(
                                accuracy,
                                1
                            )
                        ),

                    "power":
                        float(
                            round(
                                power,
                                2
                            )
                        ),

                    "duration":
                        float(
                            round(
                                duration,
                                2
                            )
                        ),

                    "time":
                        datetime.now().strftime(
                            "%I:%M:%S %p"
                        )
                }


                # Reset detector

                sneeze_active = False

                sneeze_start = None

                last_loud_time = None

                peak_rms = 0


    # =========================
    # START MICROPHONE
    # =========================

    print("🎤 Microphone ready")

    print("🤧 Waiting for sneeze...")


    with sd.InputStream(

        samplerate=SAMPLE_RATE,

        blocksize=BLOCK_SIZE,

        channels=1,

        dtype="float32",

        callback=audio_callback

    ):

        # Wait until sneeze is detected

        while result is None:

            time.sleep(0.03)


    return result