import os
import re
import subprocess
from google.cloud import speech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"
client = speech.SpeechClient()

def convert_audio_to_flac(audio_path):
    """Converts any audio file to FLAC format for Google Speech API."""
    output_path = audio_path.rsplit(".", 1)[0] + ".flac" 
    
    command = [
        "ffmpeg", "-y", "-i", audio_path, 
        "-ar", "16000",  #convert sample rate to 16,000 Hz
        "-ac", "1",  #convert to mono audio
        "-c:a", "flac",  #use flac codec
        output_path
    ]

    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if process.returncode != 0:
        raise Exception(f"FFmpeg conversion failed: {process.stderr.decode()}")

    return output_path

def transcribe_audio(audio_path):
    """Processes an audio file and returns a transcript."""
    audio_path = convert_audio_to_flac(audio_path)
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()

    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,  
        sample_rate_hertz=16000,  
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)

    if not response.results:
        return "No speech detected."

    return response.results[0].alternatives[0].transcript

def extract_details(text):
    """Extracts amount, category, and determines debit/credit from speech text."""
    amount_match = re.search(r'(\d+)\s?(rs|rupees|dollars|₹|\$)?', text, re.IGNORECASE)
    amount_value = int(amount_match[1]) if amount_match else 0
    categories = ['food', 'shopping', 'rent', 'travel', 'entertainment', 'groceries']
    category = next((cat for cat in categories if cat in text.lower()), "Unknown")
    if any(word in text.lower() for word in ["spent", "bought", "paid"]):
        amount_value = -amount_value  #debit
    elif any(word in text.lower() for word in ["received", "credited", "earned"]):
        amount_value = abs(amount_value)  #credit

    return {"amount": amount_value, "category": category}
