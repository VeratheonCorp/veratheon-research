import os
import requests
from dotenv import load_dotenv
import logging as log
from typing import Dict, Any
from urllib.parse import parse_qsl

class AlphaVantageClient: 
    def __init__(self) -> None:
        load_dotenv()  # Load environment variables
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY not found in environment.")
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query?function="
        self.session = requests.Session()

    def run_query(self, query: str) -> Dict[str, Any]:
        """Execute an Alpha Vantage API query with automatic API key insertion.
        
        Returns:
            Union[Dict[str, Any], str]: Parsed JSON response as dict if content is JSON, 
                                      otherwise returns raw response text (e.g., for CSV)
        """
        response = self.session.get(self.base_url + query + f"&apikey={self.api_key}")
        response.raise_for_status()
        
        # Check if response is JSON
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            return response.json()
        return response.text





