import os
import tempfile
from gtts import gTTS
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables from .env if needed
load_dotenv()

# --- ✅ Transcribe audio using SpeechRecognition ---
def transcribe_audio(file):
    """
    Transcribes audio file input using Google Speech Recognition API (free).
    Expects a WAV or compatible audio format in file-like object.
    """
    recognizer = sr.Recognizer()
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(file.read())
            tmp.flush()
            
            with sr.AudioFile(tmp.name) as source:
                audio = recognizer.record(source)
                
                try:
                    text = recognizer.recognize_google(audio)
                    return text
                except sr.UnknownValueError:
                    return "❌ Could not understand the audio."
                except sr.RequestError as e:
                    return f"❌ Recognition error: {e}"
    except Exception as e:
        return f"❌ Error processing audio: {e}"

# --- ✅ Text-to-Speech using gTTS ---
def text_to_speech(text):
    """
    Converts given text to speech and saves it as 'response.mp3'.
    Returns path to the MP3 file.
    """
    try:
        output_dir = "audio"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, "response.mp3")

        tts = gTTS(text)
        tts.save(file_path)

        return file_path
    except Exception as e:
        return f"❌ TTS generation failed: {e}"

# --- Optional test ---
if __name__ == "__main__":
    # Test TTS
    path = text_to_speech("Hello, your health tip is to drink water regularly.")
    print(f"Generated: {path}")
