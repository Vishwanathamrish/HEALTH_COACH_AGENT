import random
import csv
import os
from datetime import datetime

# Sample hardcoded health tips
tips_data = [
    {"tip": "Drink at least 8 glasses of water daily to stay hydrated.", "category": "Hydration"},
    {"tip": "Include fruits and vegetables in every meal.", "category": "Nutrition"},
    {"tip": "Get at least 7-8 hours of sleep each night.", "category": "Sleep"},
    {"tip": "Take short walks after meals to aid digestion.", "category": "Exercise"},
    {"tip": "Practice mindfulness or meditation for 10 minutes daily.", "category": "Mental Health"},
]

def get_daily_tip(category=None):
    """
    Returns a random health tip based on an optional category.
    Logs the selected tip for analytics.
    """
    if category:
        filtered = [tip for tip in tips_data if tip["category"].lower() == category.lower()]
        if filtered:
            tip = random.choice(filtered)
        else:
            tip = {"tip": f"No tips available for the category '{category}'.", "category": category}
    else:
        tip = random.choice(tips_data)

    log_tip_usage(tip)
    return tip

def log_tip_usage(tip):
    """
    Logs the usage of a tip to data/tip_log.csv.
    Creates the data folder if it doesn't exist.
    """
    log_path = "data/tip_log.csv"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tip.get("tip", ""),
            tip.get("category", "General")
        ])

# Optional test run
if __name__ == "__main__":
    test_tip = get_daily_tip()
    print("🩺 Daily Tip:", test_tip["tip"])


