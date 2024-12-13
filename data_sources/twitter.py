from prefect import task
from typing import Dict

@task(name="Twitter Data Fetcher")
def fetch_twitter_data(name: str) -> Dict:
    print("Fetching data from Twitter for:", name)
    # Twitter-specific fetching logic here
    return {
        "platform": "twitter",
        "data": [],
        "metadata": {
            "source": "twitter",
            "timestamp": "2024-03-21"
        }
    } 