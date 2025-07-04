import requests
from typing import Dict, Any
import logging

# Configure logging with default level DEBUG
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_categories(language: str = "en") -> Dict[str, Any]:
    """
    Fetch categories from data.gov.hk based on the specified language.

    Args:
        language: The language code for the categories list (en, tc, sc). Defaults to 'en'.

    Returns:
        Dict containing the categories data.
    """
    logger.debug(f"Fetching categories for language: {language}")
    url_map = {
        "en": "https://data.gov.hk/filestore/json/categories_en.json",
        "tc": "https://data.gov.hk/filestore/json/categories_tc.json",
        "sc": "https://data.gov.hk/filestore/json/categories_sc.json"
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
        logger.debug(f"Successfully fetched categories data from {url}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch categories data: {e}")
        return {"error": f"Failed to fetch categories data: {e}"}
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching categories: {e}")
        return {"error": f"An unexpected error occurred: {e}"}
