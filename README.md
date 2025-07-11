
# 🧘‍♀️  AI Health & Wellness Coach

Welcome to the **AI Health & Wellness Coach** — a personal health tracker and intelligent assistant powered by **Streamlit**, **LLMs**, and **Data Visualization**.  
It allows users to log daily health metrics, receive category-based health tips, view progress trends, and interact with an AI coach for personalized wellness support.


---

## 📦 Features

### ✅ Health Logging
- Record sleep hours, meals, mood, and steps.
- Logs are saved in CSV format (`user_logs.csv`).

### 💡 Daily Health Tips
- Get a random tip by category (Hydration, Nutrition, Sleep, Mental Health, Exercise).
- health tips are not repeated (stored in `health_tips.csv`).
- Tip logs are recorded for reference.

### 🔊 Voice Assistant
- Converts health tips to speech using `gTTS`.
- Allows users to listen to tips aloud in the app.

### 🧠 AI Chat Coach
- Interact with an AI-powered health assistant using Ollama + Mistral.
- Supports recall of previous chat history.
- You can request:  
  `“Show last 3 chats”`, `“I want the last chat”`, etc.

### 📈 Wellness Dashboard
- Line charts for:
  - 💤 Sleep trend
  - 🚶 Steps trend
- Bar chart for:
  - 😊 Mood distribution

---

## 🛠 Tech Stack

| Component     | Purpose                                            |
|---------------|----------------------------------------------------|
| 🐍 Python      | Backend logic                                      |
| 🖼️ Streamlit   | Web UI framework                                   |
| 📊 Matplotlib | Visualize health metrics                           |
| 🗂 Pandas      | Handle CSV log data                                |
| 🔊 gTTS        | Convert tips into speech audio                     |
| 🧠 LangChain   | (Optional) prompt routing + memory for LLM agents  |
| 🧠 Ollama      | Run Mistral or other local LLMs                    |

---

## 🧠 AI Model Used

- **Mistral (via Ollama)**  
  A fast and lightweight local LLM model.  
  Model used: `mistral:latest`

> Ollama allows you to run LLMs locally without external APIs.
> For different models (e.g., GPT-4, Claude), update `health_agent.py`.

---
## 📁 Project Structure

```bash
.
├── main.py                  # Main Streamlit app
├── requirements.txt         # All dependencies
├── agent/                   
│   ├── tools.py             # Health tips logic
│   ├── chat_utils.py        # Chat memory save/load
│   ├── health_agent.py      # AI response system
│   └── voice_tools.py       # gTTS speech handler
├── data/                    # ✅ Auto-created if not present
│   ├── user_logs.csv        # Stores wellness logs (sleep, meals, mood, steps)
│   ├── tip_log.csv          # Records shown health tips with timestamps
│   └── chat_history.csv     # Persistent chat memory
│   └── health_tips.csv      # Health tips with 'tip' and 'category' columns

---
## 🚀 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/your-username/health-coach-agent.git
cd health-coach-agent


# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
```

---

## 📝 Requirements

```
# --- Core App Dependencies ---
streamlit==1.35.0           # UI framework for building the web app
pandas==2.2.2               # Data manipulation and CSV handling
matplotlib==3.9.0           # Data visualization (line plots and charts)

# --- AI & LLM Integration ---
langchain==0.2.3            # Framework for building LLM-powered agents and chains
langchain-community==0.2.3  # Integrations like Ollama, used via LangChain
ollama==0.1.9               # Local interface for running models like Mistral
openai==1.30.1              # (Optional) API access to OpenAI GPT models

# --- Voice Features ---
gTTS==2.5.1                 # Google Text-to-Speech for audio tips
SpeechRecognition==3.10.0   # Speech-to-text capabilities (if added later)

# --- Utility Libraries ---
python-dotenv==1.0.1        # Load environment variables from .env
requests==2.31.0            # Send HTTP requests (e.g., to APIs)
PyYAML==6.0.1               # Handle YAML config files (optional/future use)
tqdm==4.66.4                # Progress bars (for future data tasks)
toolz==0.12.1               # Functional utilities (used in LangChain or extensions)
```


---

## 📌 Future Enhancements

- ✅ User authentication system
- ✅ Replace CSVs with SQLite or MySQL Worj=kbench
- ✅ Weekly email summaries (via SMTP or SendGrid)
- ✅ Mood forecasting using LSTM or Prophet
- ✅ Mobile UI optimization
- ✅ Integration with Fitbit/Apple Health APIs



---

## 👨‍💻 Author

**Vishwanath R**  
AI Engineer @ DigiDara Technologies Pvt. Ltd  
📧 vishwanathamrish@gmail.com  
🔗 [LinkedIn Profile](https://linkedin.com/in/vishwanath-r-4a940721b)
