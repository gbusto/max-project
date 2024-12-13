from prefect import task
from typing import Dict

@task(name="YouTube Data Fetcher")
def fetch_youtube_data(name: str) -> Dict:
    print("Fetching data from YouTube for:", name)
    # YouTube-specific fetching logic here
    return {
        "platform": "youtube",
        "data": [],
        "metadata": {
            "source": "youtube",
            "timestamp": "2024-03-21"
        }
    } 