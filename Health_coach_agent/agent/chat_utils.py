# agent/chat_utils.py
import os
import csv
from datetime import datetime

CHAT_LOG_PATH = "data/chat_history.csv"

def save_message(user_msg, bot_msg):
    os.makedirs("data", exist_ok=True)
    with open(CHAT_LOG_PATH, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user", user_msg])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "bot", bot_msg])

def load_chat_history():
    if not os.path.exists(CHAT_LOG_PATH):
        return []
    with open(CHAT_LOG_PATH, "r", encoding="utf-8") as f:
        return list(csv.reader(f))
