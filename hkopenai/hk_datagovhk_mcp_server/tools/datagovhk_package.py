"""
Fetch package data from data.gov.hk API.

This module retrieves detailed package info from data.gov.hk using package IDs.
"""

import logging
from typing import Dict, Any
import requests

# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_package_data(package_id: str, language: str = "en") -> Dict[str, Any]:
    """
    Fetch package data from data.gov.hk API using the provided ID and language.

    Args:
        package_id: The ID of the package to fetch data for.
        language: The language code (en, tc, sc) to fetch the data in. Defaults to "en".

    Returns:
        Dict containing the package data.
    """
    logger.debug("Fetching package data for ID: %s in language: %s", package_id, language)
    if language not in ["en", "tc", "sc"]:
        logger.error("Invalid language code: %s. Defaulting to 'en'.", language)
        language = "en"
    url = f"https://data.gov.hk/{language}-data/api/3/action/package_show?id={package_id}"
    logger.debug("Using URL: %s", url)
    try:
        headers = {
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logger.debug("Successfully fetched package data from %s", url)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch package data: %s", e)
        return {"error": f"Failed to fetch package data: {str(e)}"}
    except Exception as e:
        logger.error("An unexpected error occurred while fetching package data: %s", e)
        return {"error": f"Failed to fetch package data: {str(e)}"}
