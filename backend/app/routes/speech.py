import os
import re
import shutil
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.speech_service import transcribe_audio, extract_details

router = APIRouter(prefix="/speech", tags=["Speech Recognition"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe")
async def transcribe_audio_route(file: UploadFile = File(...)):
    """Receives an audio file, processes it, and extracts expense details."""
    if not file.filename.endswith((".wav", ".flac", ".ogg", ".m4a", ".acc")):
        raise HTTPException(status_code=400, detail="Invalid file format. Use WAV, FLAC, OGG, or M4A.")
    audio_path = os.path.join(UPLOAD_DIR, f"temp_{file.filename}")
    with open(audio_path, "wb") as audio_file:
        shutil.copyfileobj(file.file, audio_file)
    transcript = transcribe_audio(audio_path)
    if transcript == "No speech detected.":
        raise HTTPException(status_code=400, detail="No speech detected. Please try again.")
    extracted_data = extract_details(transcript)
    return {"transcript": transcript, "extracted_data": extracted_data}
