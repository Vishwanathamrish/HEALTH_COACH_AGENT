import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import base64
import os

from agent.tools import get_daily_tip
from agent.voice_tools import text_to_speech
from agent.health_agent import get_agent_response
from agent.chat_utils import save_message, load_chat_history  # ✅ NEW

# --- Constants ---
LOG_FILE = "data/user_logs.csv"
COLUMNS = ["date", "sleep_hours", "meals", "mood", "steps"]

# --- Initialize Logs ---
os.makedirs("data", exist_ok=True)
if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
    pd.DataFrame(columns=COLUMNS).to_csv(LOG_FILE, index=False)

# --- Load Logs ---
df = pd.read_csv(LOG_FILE)
df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
df["sleep_hours"] = pd.to_numeric(df["sleep_hours"], errors='coerce')
df["steps"] = pd.to_numeric(df["steps"], errors='coerce')

# --- Streamlit Config ---
st.set_page_config(page_title="Health Coach Agent", page_icon="🧘‍♀️")
st.title("🧘‍♀️ AI Health & Wellness Coach")
st.markdown("Track your health, get tips, visualize progress, and talk to your personal AI coach.")

# --- Health Logging Form ---
with st.form("log_form"):
    st.subheader("📋 Daily Health Log")
    sleep_hours = st.slider("🛌 Hours of Sleep", 0, 12, 7)
    meals = st.text_input("🍱 Meals you had today")
    mood = st.selectbox("😊 Mood Today", ["Happy", "Stressed", "Tired", "Energetic", "Sad"])
    steps = st.number_input("🚶 Steps Walked", min_value=0, step=100)

    if st.form_submit_button("📂 Save Log"):
        new_data = {
            "date": datetime.today().strftime("%Y-%m-%d"),
            "sleep_hours": sleep_hours,
            "meals": meals,
            "mood": mood,
            "steps": steps
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(LOG_FILE, index=False)
        st.success("✅ Your daily log was saved!")

# --- Show Logs ---
st.subheader("📊 Your Recent Wellness Log")
if df.empty:
    st.warning("No health logs yet. Fill in the form above to start tracking.")
else:
    st.dataframe(df.tail(7), use_container_width=True)

    # --- Clear Log Button ---
    if st.button("🧹 Clear Wellness Log"):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(LOG_FILE, index=False)
        st.success("✅ Wellness log has been cleared!")
        


# --- Daily Tip Section ---
from agent.tools import get_daily_tip  # ✅ Only this is needed

st.subheader("💡 Daily Health Tip")
category = st.selectbox("Filter tip by category", ["All", "Hydration", "Nutrition", "Exercise", "Sleep", "Mental Health"])
filtered_category = None if category == "All" else category

tip_data = get_daily_tip(filtered_category)
st.info(tip_data["tip"])

# 🔊 Hear the tip aloud
if st.checkbox("🔊 Hear the tip aloud", key="hear_tip"):
    try:
        mp3_path = text_to_speech(tip_data["tip"])
        with open(mp3_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            audio_html = f"""
            <audio autoplay controls>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to generate audio: {e}")

# # --- Voice Playback Option ---
# if st.checkbox("🔊 Hear the tip aloud"):
#     try:
#         mp3_path = text_to_speech(tip_data["tip"])
#         with open(mp3_path, "rb") as f:
#             b64 = base64.b64encode(f.read()).decode()
#             audio_html = f"""
#             <audio autoplay controls>
#             <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
#             </audio>
#             """
#             st.markdown(audio_html, unsafe_allow_html=True)
#     except Exception as e:
#         st.error(f"Failed to generate audio: {e}")

# --- Persistent Chat Section ---
st.subheader("💬 Chat with AI Health Coach")

# Load previous chat into session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

# Show previous messages
for timestamp, role, message in st.session_state.chat_history[-10:]:  # last 10 messages
    if role == "user":
        st.markdown(f"👤 **You** ({timestamp}): {message}")
    else:
        st.markdown(f"🤖 **Coach** ({timestamp}): {message}")

# Input + Response
user_query = st.text_input("Type your message:", key="chat_input")
if user_query:
    lowered_query = user_query.lower()

    # Check for requests like "last 3 chat", "show last 5 chats", etc.
    import re
    match = re.search(r'last\s+(\d+)\s+chat', lowered_query)
    if lowered_query in [
        "show last chat", "last chat", 
        "what was our last conversation?", 
        "i want a last chat"
    ] or match:
        # Determine how many pairs to show
        num_pairs = 1
        if match:
            num_pairs = int(match.group(1))
        
        chat_history = st.session_state.chat_history
        if chat_history:
            last_messages = chat_history[-2*num_pairs:]
            for timestamp, role, message in last_messages:
                speaker = "👤 You" if role == "user" else "🤖 Coach"
                st.success(f"{speaker} ({timestamp}): {message}")
        else:
            st.warning("No previous chat found.")
    else:
        with st.spinner("🧠 Thinking..."):
            try:
                response = get_agent_response(user_query, df)
                st.success(f"🤖 Coach: {response}")
                # Save to memory and file
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.chat_history.append([timestamp, "user", user_query])
                st.session_state.chat_history.append([timestamp, "bot", response])
                save_message(user_query, response)
            except Exception as e:
                st.error(f"❌ Error from agent: {e}")


# Clear Chat Option
if st.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
    if os.path.exists("data/chat_history.csv"):
        os.remove("data/chat_history.csv")
    st.success("Chat history cleared!")

# --- Analytics Dashboard ---
if not df.empty:
    st.subheader("📈 Wellness Dashboard (Last 7 Days)")
    last_7 = df.tail(7).copy()
    dates_str = last_7["date"].astype(str)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Sleep Hours**")
        fig1, ax1 = plt.subplots()
        ax1.plot(dates_str, last_7["sleep_hours"], marker='o', color='blue')
        ax1.set_xticks(range(len(dates_str)))
        ax1.set_xticklabels(dates_str, rotation=45)
        st.pyplot(fig1)

    with col2:
        st.markdown("**Steps Walked**")
        fig2, ax2 = plt.subplots()
        ax2.plot(dates_str, last_7["steps"], marker='o', color='green')
        ax2.set_xticks(range(len(dates_str)))
        ax2.set_xticklabels(dates_str, rotation=45)
        st.pyplot(fig2)

    st.markdown("**🧠 Mood Distribution**")
    st.bar_chart(last_7["mood"].value_counts())

# --- Footer ---
st.markdown("---")
st.caption("🚀 Built with Streamlit, Ollama + Mistral, gTTS, LangChain, and CSV memory")
