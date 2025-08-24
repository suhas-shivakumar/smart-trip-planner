from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import os
import logging
from dotenv import load_dotenv

load_dotenv()
token_url = os.getenv("ACCESS_TOKEN_URL")
client_id = os.getenv("AMADEUS_CLIENT_ID")
client_secret = os.getenv("AMADEUS_CLIENT_SECRET")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_token():
    """
    Fetch OAuth token from Amadeus API using client credentials.
    Returns the access token string, or None if an error occurs.
    """
    try:
        logger.info(f"Requesting OAuth token from Amadeus...")

        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url=token_url,
            client_id=client_id,
            client_secret=client_secret,
            verify=False,
        )
        logger.info(f"Successfully obtained Amadeus API token...")
        return token["access_token"]
    except Exception as e:
        logger.info(f"Error while fetching the token due to: {e}")
        return None
