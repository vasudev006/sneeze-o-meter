from analyzer import analyze_sneeze

test_result = {
    "accuracy": 95.4,
    "power": 8.72,
    "duration": 0.52,
    "time": "07:20:15 PM"
}

result = analyze_sneeze(test_result)

print("\n🤧 SNEEZE ANALYSIS")
print("Personality:", result["personality"])
print("Description:", result["description"])
print("Award:", result["award"])