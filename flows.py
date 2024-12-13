from prefect import flow, task
from typing import List, Dict

# Input Phase Tasks
@task(name="Validate Input")
def validate_input(name: str) -> str:
    print("Executing: Validate Input")
    return name


# Data Collection Phase Tasks
@task(name="Fetch Twitter Data")
def fetch_twitter_data(name: str) -> Dict:
    print("Executing: Fetch Twitter Data")
    return {"platform": "twitter", "data": []}


@task(name="Fetch Articles")
def fetch_articles(name: str) -> Dict:
    print("Executing: Fetch Articles")
    return {"platform": "articles", "data": []}


@task(name="Fetch YouTube Data")
def fetch_youtube_data(name: str) -> Dict:
    print("Executing: Fetch YouTube Data")
    return {"platform": "youtube", "data": []}


@task(name="Fetch Podcast Data")
def fetch_podcast_data(name: str) -> Dict:
    print("Executing: Fetch Podcast Data")
    return {"platform": "podcast", "data": []}


# Data Cleaning Phase Tasks
@task(name="Clean and Consolidate Data")
def clean_and_consolidate(raw_data: List[Dict]) -> Dict:
    print("Executing: Clean and Consolidate Data")
    return {"cleaned_data": []}


# Claim Extraction Phase Tasks
@task(name="Extract Claims")
def extract_claims(cleaned_data: Dict) -> List[Dict]:
    print("Executing: Extract Claims")
    return []


@task(name="Deduplicate Claims")
def deduplicate_claims(claims: List[Dict]) -> List[Dict]:
    print("Executing: Deduplicate Claims")
    return []


# Claim Verification Phase Tasks
@task(name="Verify Claims")
def verify_claims(claims: List[Dict]) -> List[Dict]:
    print("Executing: Verify Claims")
    return []


# Output Phase Tasks
@task(name="Save Results")
def save_results(verified_claims: List[Dict]) -> bool:
    print("Executing: Save Results")
    return True


@task(name="Generate Report")
def generate_report(verified_claims: List[Dict]) -> str:
    print("Executing: Generate Report")
    return "Report generated"


# Notification Tasks
@task(name="Send Notifications")
def send_notifications(report_path: str) -> None:
    print("Executing: Send Notifications")


@flow(name="Influencer Analysis Pipeline")
def analyze_influencer(name: str):
    # Input Phase
    validated_name = validate_input(name)
    
    # Data Collection Phase
    twitter_data = fetch_twitter_data(validated_name)
    articles_data = fetch_articles(validated_name)
    youtube_data = fetch_youtube_data(validated_name)
    podcast_data = fetch_podcast_data(validated_name)
    
    # Data Cleaning Phase
    raw_data = [twitter_data, articles_data, youtube_data, podcast_data]
    cleaned_data = clean_and_consolidate(raw_data)
    
    # Claim Extraction Phase
    claims = extract_claims(cleaned_data)
    unique_claims = deduplicate_claims(claims)
    
    # Claim Verification Phase
    verified_claims = verify_claims(unique_claims)
    
    # Output Phase
    save_results(verified_claims)
    report = generate_report(verified_claims)
    
    # Notifications
    send_notifications(report)
    
    return report
