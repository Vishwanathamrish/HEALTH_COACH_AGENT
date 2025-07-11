import random
import pandas as pd
import os
import csv
from datetime import datetime

# --- Paths ---
TIPS_FILE = "data/health_tips.csv"
LOG_FILE = "data/tip_log.csv"

# --- Load all tips from the CSV file ---
def load_health_tips():
    if not os.path.exists(TIPS_FILE):
        raise FileNotFoundError(f"❌ CSV file not found: {TIPS_FILE}")
    
    df = pd.read_csv(TIPS_FILE)
    df.columns = [col.strip().lower() for col in df.columns]
    
    if "tip" not in df.columns or "category" not in df.columns:
        raise ValueError("❌ CSV must have 'tip' and 'category' columns.")
    
    return df

# --- Log selected tip to usage file ---
def log_tip_usage(tip):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tip.get("tip", ""),
            tip.get("category", "General")
        ])

# --- Get a random tip (with optional category) ---
def get_daily_tip(category=None):
    tips_df = load_health_tips()

    if category:
        filtered_df = tips_df[tips_df["category"].str.lower() == category.lower()]
        if filtered_df.empty:
            return {
                "tip": f"No tips available for the category '{category}'.",
                "category": category
            }
        selected = filtered_df.sample(1).iloc[0]
    else:
        selected = tips_df.sample(1).iloc[0]

    tip_data = {
        "tip": selected["tip"],
        "category": selected["category"]
    }

    log_tip_usage(tip_data)
    return tip_data

# --- Test Run ---
if __name__ == "__main__":
    tip = get_daily_tip()
    print("💡 Daily Tip:", tip["tip"])
