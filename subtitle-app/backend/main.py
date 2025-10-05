import os
import requests
import tempfile
from typing import Dict, List, Optional, Union
from datetime import timedelta
import subprocess
import base64
import json
import asyncio
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

# Import our existing classes
import sys
sys.path.append('..')
from subtitle import (
    SubtitleTranslator, 
    ElevenLabsSubtitleGenerator,
    TARGET_LANGUAGES,
    TRANSLATION_SERVICES,
    generate_srt_subtitles,
    generate_vtt_subtitles,
    translate_subtitles_preserve_structure,
    parse_srt_subtitles,
    extract_audio_from_video
)

app = FastAPI(title="Subtitle Generator API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class TranscriptionRequest(BaseModel):
    api_key: str
    language_code: Optional[str] = None
    num_speakers: Optional[int] = None
    diarize: bool = True
    tag_audio_events: bool = True

class TranslationRequest(BaseModel):
    srt_content: str
    target_languages: List[str]
    translation_service: str = "google_free"
    api_key: Optional[str] = None

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict] = None

# Global storage for session data
sessions = {}

@app.get("/")
async def root():
    return {"message": "Subtitle Generator API is running"}

@app.get("/api/languages")
async def get_languages():
    """Get supported languages for transcription and translation"""
    transcription_languages = {
        "Auto-detect": None,
        "English": "eng", "Spanish": "spa", "French": "fra", "German": "deu",
        "Italian": "ita", "Portuguese": "por", "Russian": "rus", "Japanese": "jpn",
        "Chinese (Mandarin)": "zho", "Korean": "kor", "Hindi": "hin", "Arabic": "ara",
        "Dutch": "nld", "Turkish": "tur", "Polish": "pol", "Swedish": "swe",
        "Norwegian": "nor", "Danish": "dan", "Finnish": "fin", "Czech": "ces",
        "Hungarian": "hun", "Bulgarian": "bul", "Romanian": "ron", "Greek": "ell",
        "Hebrew": "heb", "Thai": "tha", "Vietnamese": "vie", "Indonesian": "ind",
        "Malay": "msa", "Filipino": "fil", "Ukrainian": "ukr", "Bengali": "ben",
        "Afrikaans": "afr", "Amharic": "amh", "Armenian": "hye", "Assamese": "asm",
        "Azerbaijani": "aze", "Belarusian": "bel", "Bosnian": "bos", "Burmese": "mya",
        "Catalan": "cat", "Croatian": "hrv", "Estonian": "est", "Georgian": "kat",
        "Gujarati": "guj", "Icelandic": "isl", "Irish": "gle", "Javanese": "jav",
        "Kannada": "kan", "Kazakh": "kaz", "Khmer": "khm", "Latvian": "lav",
        "Lithuanian": "lit", "Macedonian": "mkd", "Malayalam": "mal", "Maltese": "mlt",
        "Marathi": "mar", "Mongolian": "mon", "Nepali": "nep", "Persian": "fas",
        "Punjabi": "pan", "Serbian": "srp", "Slovak": "slk", "Slovenian": "slv",
        "Swahili": "swa", "Tamil": "tam", "Telugu": "tel", "Urdu": "urd",
        "Welsh": "cym", "Zulu": "zul"
    }
    
    return APIResponse(
        success=True,
        message="Languages retrieved successfully",
        data={
            "transcription_languages": transcription_languages,
            "translation_languages": TARGET_LANGUAGES,
            "translation_services": TRANSLATION_SERVICES
        }
    )

@app.post("/api/transcribe")
async def create_transcription(
    file: UploadFile = File(...),
    api_key: str = Form(...),
    language_code: Optional[str] = Form(None),
    num_speakers: Optional[int] = Form(None),
    diarize: bool = Form(True),
    tag_audio_events: bool = Form(True)
):
    """Create transcription from uploaded audio/video file"""
    try:
        if not api_key or api_key == "your_api_key_here":
            raise HTTPException(status_code=400, detail="Valid ElevenLabs API key required")
        
        # Create session ID
        session_id = str(uuid.uuid4())
        
        # Read file content
        file_content = await file.read()
        
        # Extract audio if video file
        if file.content_type and file.content_type.startswith('video/'):
            try:
                file_content = extract_audio_from_video(file_content)
            except Exception as e:
                # Continue with original file if extraction fails
                pass
        
        # Initialize generator
        generator = ElevenLabsSubtitleGenerator(api_key)
        
        # Create transcription
        transcription = generator.create_transcription(
            file_content,
            language_code=language_code,
            num_speakers=num_speakers,
            diarize=diarize,
            tag_audio_events=tag_audio_events
        )
        
        # Generate subtitle formats
        srt_content = generate_srt_subtitles(transcription)
        vtt_content = generate_vtt_subtitles(transcription)
        
        # Store in session
        sessions[session_id] = {
            'transcription': transcription,
            'srt_content': srt_content,
            'vtt_content': vtt_content,
            'filename': file.filename
        }
        
        # Calculate statistics
        speakers = set()
        if 'words' in transcription:
            for word in transcription['words']:
                if word.get('speaker_id'):
                    speakers.add(word['speaker_id'])
        
        duration = 0
        if 'words' in transcription and transcription['words']:
            duration = transcription['words'][-1].get('end', 0)
        
        return APIResponse(
            success=True,
            message="Transcription completed successfully",
            data={
                'session_id': session_id,
                'language': transcription.get('language_code', 'Unknown'),
                'confidence': transcription.get('language_probability', 0),
                'speakers_detected': len(speakers),
                'duration': duration,
                'srt_content': srt_content,
                'vtt_content': vtt_content,
                'transcription': transcription
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/translate")
async def translate_subtitles(
    session_id: str = Form(...),
    target_languages: str = Form(...),  # JSON string of list
    translation_service: str = Form("google_free"),
    api_key: Optional[str] = Form(None)
):
    """Translate subtitles to multiple languages"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Parse target languages from JSON string
        target_languages_list = json.loads(target_languages)
        
        session_data = sessions[session_id]
        srt_content = session_data['srt_content']
        
        translated_subtitles = {}
        translated_vtt = {}
        
        for lang in target_languages_list:
            try:
                # Translate while preserving structure
                translated_srt = translate_subtitles_preserve_structure(
                    srt_content,
                    lang,
                    translation_service,
                    api_key
                )
                
                if translated_srt and translated_srt != srt_content:
                    translated_subtitles[lang] = translated_srt
                    
                    # Convert to VTT format
                    vtt_content = "WEBVTT\n\n"
                    lines = translated_srt.strip().split('\n')
                    for line in lines:
                        if '-->' in line:
                            vtt_line = line.replace(',', '.')
                            vtt_content += vtt_line + '\n'
                        else:
                            vtt_content += line + '\n'
                    translated_vtt[lang] = vtt_content
                    
            except Exception as e:
                print(f"Failed to translate to {lang}: {str(e)}")
                continue
        
        # Update session with translations
        sessions[session_id]['translated_subtitles'] = translated_subtitles
        sessions[session_id]['translated_vtt'] = translated_vtt
        
        return APIResponse(
            success=True,
            message=f"Translation completed for {len(translated_subtitles)} languages",
            data={
                'translated_subtitles': translated_subtitles,
                'translated_vtt': translated_vtt,
                'success_count': len(translated_subtitles),
                'total_requested': len(target_languages_list)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get session data"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return APIResponse(
        success=True,
        message="Session data retrieved",
        data=sessions[session_id]
    )

@app.get("/api/download/{session_id}/{format}/{language}")
async def download_subtitle(session_id: str, format: str, language: str = "original"):
    """Download subtitle file"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    filename_base = session_data['filename'].split('.')[0] if session_data['filename'] else 'subtitle'
    
    try:
        if language == "original":
            if format == "srt":
                content = session_data['srt_content']
                filename = f"{filename_base}.srt"
            elif format == "vtt":
                content = session_data['vtt_content']
                filename = f"{filename_base}.vtt"
            elif format == "json":
                content = json.dumps(session_data['transcription'], indent=2)
                filename = f"{filename_base}.json"
            else:
                raise HTTPException(status_code=400, detail="Invalid format")
        else:
            # Translated subtitle
            if format == "srt":
                content = session_data['translated_subtitles'][language]
                filename = f"{filename_base}_{language}.srt"
            elif format == "vtt":
                content = session_data['translated_vtt'][language]
                filename = f"{filename_base}_{language}.vtt"
            else:
                raise HTTPException(status_code=400, detail="Invalid format for translation")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=f'.{format}', encoding='utf-8') as tmp_file:
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        return FileResponse(
            path=tmp_file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Translation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)