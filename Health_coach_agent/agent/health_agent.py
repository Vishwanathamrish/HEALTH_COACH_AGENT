import random
import json
import os
import pandas as pd
from langchain_community.llms import Ollama

# --- Load health tips from JSON ---
def load_health_tips():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    filepath = os.path.join(base_dir, "assets", "health_tips.json")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        tips = json.load(f)

    if not isinstance(tips, list):
        raise ValueError("❌ JSON content must be a list of tips.")

    return tips

# --- Get a daily tip ---
def get_daily_tip():
    tips = load_health_tips()
    return random.choice(tips) if tips else "No tips available today."

# --- Set up Ollama model ---
llm = Ollama(model="mistral", temperature=0.7)

# --- Generate a response from the agent ---
def get_agent_response(query, user_df):
    try:
        temp_path = "data/temp_user_data.csv"
        user_df.to_csv(temp_path, index=False)

        # Format recent health data
        df_cleaned = user_df.copy()
        df_cleaned["date"] = pd.to_datetime(df_cleaned["date"], errors="coerce").dt.strftime("%Y-%m-%d")
        df_cleaned["sleep_hours"] = pd.to_numeric(df_cleaned["sleep_hours"], errors='coerce')
        df_cleaned["steps"] = pd.to_numeric(df_cleaned["steps"], errors='coerce')
        context = df_cleaned.tail(7).fillna("N/A").to_string(index=False)

        prompt = f"""
You are a friendly and helpful AI Health Coach.

Here is the user's recent health log:

{context}

User's Question:
{query}

Please provide useful, actionable advice in simple terms.
"""

        response = llm.invoke(prompt)
        return response.strip().replace("\n", " ")

    except Exception as e:
        return f"❌ Ollama/Mistral Error: {e}"

# --- Local test ---
if __name__ == "__main__":
    try:
        print("💡 Daily Health Tip:", get_daily_tip())
    except Exception as e:
        print("⚠️ Error:", e)
