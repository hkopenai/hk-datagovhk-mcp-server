import requests
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_providers(language: str = "en") -> Dict[str, Any]:
    """
    Fetch providers from data.gov.hk based on the specified language.

    Args:
        language: The language code for the providers list (en, tc, sc). Defaults to 'en'.

    Returns:
        Dict containing the providers data.
    """
    logger.debug(f"Fetching providers for language: {language}")
    url_map = {
        "en": "https://data.gov.hk/filestore/json/providers_en.json",
        "tc": "https://data.gov.hk/filestore/json/providers_tc.json",
        "sc": "https://data.gov.hk/filestore/json/providers_sc.json"
    }
    url = url_map.get(language, url_map["en"])
    logger.debug(f"Using URL: {url}")
    
    try:
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.debug(f"Successfully fetched providers data from {url}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch providers data: {e}")
        return {"error": f"Failed to fetch providers data: {e}"}
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching providers: {e}")
        return {"error": f"An unexpected error occurred: {e}"}
