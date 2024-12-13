from prefect import task
from typing import Dict, List
import hashlib
import time
import requests
import json
import os
from datetime import datetime
from .base import create_response_template, DataSourceError
from .utils.transcription import transcribe_audio

def extract_podcast_urls(response_data: Dict) -> List[str]:
    """Extract enclosure URLs from podcast response data"""
    urls = []
    if response_data.get("status") == "true" and "items" in response_data:
        for item in response_data["items"]:
            if url := item.get("enclosureUrl"):
                urls.append(url)
    return urls

@task(name="Podcast Data Fetcher")
def fetch_podcast_data(name: str) -> Dict:
    print("Fetching podcast data for:", name)
    
    # Get API credentials from environment variables
    api_key = os.getenv('PODCAST_INDEX_API_KEY')
    api_secret = os.getenv('PODCAST_INDEX_API_SECRET')
    
    if not api_key or not api_secret:
        raise DataSourceError("Missing Podcast Index API credentials")
    
    # Setup the API request
    MAX_RESULTS = 1
    base_url = "https://api.podcastindex.org/api/1.0/search/byperson"
    url = f"{base_url}?q={name}&max={MAX_RESULTS}"
    
    # Generate authentication headers
    epoch_time = int(time.time())
    data_to_hash = api_key + api_secret + str(epoch_time)
    sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()
    
    headers = {
        'X-Auth-Date': str(epoch_time),
        'X-Auth-Key': api_key,
        'Authorization': sha_1,
        'User-Agent': 'influencer-analysis-tool'
    }
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        
        podcast_data = response.json()
        podcast_urls = extract_podcast_urls(podcast_data)
        
        # Transcribe each podcast
        transcripts = []
        for url in podcast_urls:
            try:
                print(f"Transcribing {url}...")
                transcript = transcribe_audio(url)
                transcripts.append({
                    "url": url,
                    "transcript": transcript
                })
            except Exception as e:
                print(f"Error transcribing {url}: {str(e)}")
                transcripts.append({
                    "url": url,
                    "error": str(e)
                })
        
        return create_response_template(
            source="podcasts",
            data={
                "raw_response": podcast_data,
                "podcast_urls": podcast_urls,
                "transcripts": transcripts
            }
        )
        
    except requests.RequestException as e:
        print(f"Error fetching podcast data: {str(e)}")
        return create_response_template(
            source="podcasts",
            data={
                "error": str(e),
                "podcast_urls": [],
                "transcripts": []
            }
        )