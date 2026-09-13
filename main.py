from flask import Flask, render_template, jsonify

from detector import detect_sneeze
from analyzer import analyze_sneeze

import threading


# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)


# =====================================================
# GLOBAL RESULT
# =====================================================

latest_result = None


# =====================================================
# DETECTOR THREAD
# =====================================================

def run_detector():

    global latest_result


    # Detect sneeze

    latest_result = detect_sneeze()


    # Analyze sneeze

    analysis = analyze_sneeze(
        latest_result
    )


    # Add personality + award

    latest_result.update(
        analysis
    )


# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =====================================================
# START DETECTION
# =====================================================

@app.route("/start")
def start_detection():

    global latest_result


    # Clear old result

    latest_result = None


    # Start detector

    thread = threading.Thread(
        target=run_detector
    )

    thread.daemon = True

    thread.start()


    return jsonify({

        "status":
            "listening"

    })


# =====================================================
# GET RESULT
# =====================================================

@app.route("/result")
def get_result():

    return jsonify(
        latest_result
    )


# =====================================================
# START SERVER
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )