from typing import Dict, Any
from datetime import datetime

class DataSourceError(Exception):
    """Base exception for data source errors"""
    pass

def create_response_template(source: str, data: Any) -> Dict:
    """Creates a standardized response format"""
    return {
        "platform": source,
        "data": data,
        "metadata": {
            "source": source,
            "timestamp": datetime.utcnow().isoformat()
        }
    } 