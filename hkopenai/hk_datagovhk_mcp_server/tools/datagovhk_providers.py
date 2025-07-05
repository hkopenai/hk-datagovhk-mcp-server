"""
Fetch providers from data.gov.hk API.

This module retrieves provider info from data.gov.hk in various languages.
"""

import logging
from typing import Dict, Any
import requests

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
    logger.debug("Fetching providers for language: %s", language)
    url_map = {
        "en": "https://data.gov.hk/filestore/json/providers_en.json",
        "tc": "https://data.gov.hk/filestore/json/providers_tc.json",
        "sc": "https://data.gov.hk/filestore/json/providers_sc.json"
    }
    url = url_map.get(language, url_map["en"])
    logger.debug("Using URL: %s", url)
    try:
        headers = {
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/* Safari/* Edg/*"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logger.debug("Successfully fetched providers data from %s", url)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch providers data: %s", e)
        return {"error": f"Failed to fetch providers data: {str(e)}"}
    except Exception as e:
        logger.error("An unexpected error occurred while fetching providers: %s", e)
        return {"error": f"Failed to fetch providers data: {str(e)}"}
