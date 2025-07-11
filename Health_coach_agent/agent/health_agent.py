import random
import json
import os
import pandas as pd
from langchain_community.llms import Ollama



# --- Set up Ollama model ---
llm = Ollama(model="mistral", temperature=0.7)

# --- Generate a response from the agent ---
def get_agent_response(query, user_df):
    try:
        # Clean and prepare recent health data (no CSV writing)
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



