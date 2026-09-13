import random


def analyze_sneeze(result):

    # =====================================================
    # SNEEZE PERSONALITIES
    # =====================================================

    personalities = [

        (
            "🐭 Mouse Sneeze",
            "Small, precise and suspiciously adorable.",
            "mouse"
        ),

        (
            "🚂 Train Sneeze",
            "Long, unstoppable and slightly concerning.",
            "train"
        ),

        (
            "☢️ Nuclear Sneeze",
            "Absolutely unnecessary levels of power.",
            "nuclear"
        ),

        (
            "🦁 Lion Sneeze",
            "Loud, powerful and impossible to ignore.",
            "lion"
        ),

        (
            "🦖 Dinosaur Sneeze",
            "A prehistoric level of sneeze energy.",
            "dinosaur"
        )

    ]


    # =====================================================
    # RANDOM PERSONALITY
    # =====================================================

    personality, description, gif = random.choice(
        personalities
    )


    # =====================================================
    # GET SNEEZE DATA
    # =====================================================

    power = round(float(result["power"]), 2)

    accuracy = round(float(result["accuracy"]), 2)

    duration = round(float(result["duration"]), 2)


    # =====================================================
    # SNEEZE AWARD
    # =====================================================

    if power >= 8:

        award = "💥 Most Powerful Sneeze"

    elif duration <= 0.5:

        award = "⚡ Fastest Sneeze"

    elif accuracy >= 95:

        award = "🏆 Sneeze of the Year"

    elif duration >= 1.2:

        award = "🎭 Most Dramatic Sneeze"

    else:

        award = "🔊 Loudest Sneeze"


    # =====================================================
    # RETURN
    # =====================================================

    return {

        "personality": personality,

        "description": description,

        "gif": gif,

        "award": award

    }