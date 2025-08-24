import logging
import requests
import json
import os
from utils.token import get_token
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AmadeusAPI:
    def __init__(self):
        self.base_url = os.getenv("AMADEUS_BASE_URL", "https://test.api.amadeus.com")
        self.client_id = os.getenv("AMADEUS_CLIENT_ID", "")
        self.client_secret = os.getenv("AMADEUS_CLIENT_SECRET", "")
        self.token_url = os.getenv("ACCESS_TOKEN_URL", "")
        self.session = requests.Session()

    def _get_headers(self, token: str) -> dict:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "cache-control": "no-cache",
        }

    def get(self, endpoint: str, params: dict = None) -> dict:
        """Make authenticated request to Amadeus API"""
        token = get_token()
        headers = self._get_headers(token)
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making request to: {url} with params: {params}")
        try:
            response = self.session.get(
                url, headers=headers, params=params, verify=False, timeout=30
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Network request failed: {str(e)}")
            raise Exception(f"Network request failed: {str(e)}")

        logger.info(
            f"Response status: {response.status_code}, {len(response.content)} bytes"
        )

        if response.status_code != 200:
            logger.error(
                f"API request failed with status {response.status_code}: {response.text}"
            )
            raise Exception(
                f"API request failed with status {response.status_code}: {response.text}"
            )

        if not response.content:
            logger.error("Empty response from Amadeus API")
            raise Exception("Empty response from Amadeus API")

        try:
            return response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Raw response: {response.text}")
            return {
                "raw_response": response.text,
                "status_code": response.status_code,
                "error": f"Failed to parse JSON: {str(e)}",
            }
