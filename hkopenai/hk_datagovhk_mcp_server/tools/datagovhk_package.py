import requests
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_package_data(id: str, language: str = "en") -> Dict[str, Any]:
    """
    Fetch package data from data.gov.hk API using the provided ID and language.

    Args:
        id: The ID of the package to fetch data for.
        language: The language code (en, tc, sc) to fetch the data in. Defaults to "en".

    Returns:
        Dict containing the package data.
    """
    logger.debug(f"Fetching package data for ID: {id} in language: {language}")
    if language not in ["en", "tc", "sc"]:
        logger.error(f"Invalid language code: {language}. Defaulting to 'en'.")
        language = "en"
    url = f"https://data.gov.hk/{language}-data/api/3/action/package_show?id={id}"
    logger.debug(f"Using URL: {url}")
    
    try:
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.debug(f"Successfully fetched package data from {url}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch package data: {e}")
        return {"error": f"Failed to fetch package data: {e}"}
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching package data: {e}")
        return {"error": f"An unexpected error occurred: {e}"}
