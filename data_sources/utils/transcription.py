import assemblyai as aai
import os
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import hashlib

TRANSCRIPTS_DIR = Path("data/transcripts")

def hash_url(url: str) -> str:
    """Generate a SHA-256 hash of the URL for use as a filename"""
    return hashlib.sha256(url.encode()).hexdigest()

def get_cached_transcript(url: str) -> Optional[Dict]:
    """Get transcript from cache if it exists"""
    filename = f"{hash_url(url)}.json"
    filepath = TRANSCRIPTS_DIR / filename
    
    if filepath.exists():
        print(f"Found cached transcript for {url}")
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def save_transcript(url: str, transcript_data: Dict):
    """Save transcript to cache"""
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    
    filename = f"{hash_url(url)}.json"
    filepath = TRANSCRIPTS_DIR / filename
    
    with open(filepath, 'w') as f:
        json.dump({
            "url": url,
            "transcript": transcript_data,
            "cached_at": datetime.utcnow().isoformat()
        }, f, indent=2)

def transcribe_audio(url: str) -> Dict:
    """Transcribe audio URL using AssemblyAI, with caching"""
    # Check cache first
    if cached := get_cached_transcript(url):
        return cached
    
    # Get API key from environment
    api_key = os.getenv('ASSEMBLY_AI_API_KEY')
    if not api_key:
        raise ValueError("Missing ASSEMBLY_AI_API_KEY environment variable")
    
    # Initialize transcriber
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    
    # Transcribe
    print(f"Transcribing {url}...")
    transcript = transcriber.transcribe(url)
    
    # Prepare response data
    transcript_data = {
        "text": transcript.text,
        "confidence": transcript.confidence,
        "words": transcript.words
    }
    
    # Cache the result
    save_transcript(url, transcript_data)
    
    return transcript_data 