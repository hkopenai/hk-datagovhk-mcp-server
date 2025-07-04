import requests
from typing import Dict, Any
import logging

# Configure logging with default level DEBUG
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_package_data(id: str) -> Dict[str, Any]:
    """
    Fetch package data from data.gov.hk API using the provided ID.

    Args:
        id: The ID of the package to fetch data for.

    Returns:
        Dict containing the package data.
    """
    logger.debug(f"Fetching package data for ID: {id}")
    url = f"https://data.gov.hk/en-data/api/3/action/package_show?id={id}"
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
