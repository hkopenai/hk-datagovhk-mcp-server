import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

def crawl_datasets(category: str, page: int = 1) -> Dict[str, Any]:
    """
    Crawl datasets from data.gov.hk based on category and page number using API.

    Args:
        category: The category of datasets to crawl (e.g., 'city-management').
        page: The page number to crawl (default: 1).

    Returns:
        Dict containing a list of datasets with their titles and links.
    """
    logger.debug(f"Starting crawl for category: {category}, page: {page}")
    base_url = "https://data.gov.hk/api/v1/datasets"
    limit = 12
    offset = (page - 1) * limit
    params = {
        "limit": limit,
        "offset": offset,
        "category": category,
        "lang": "en"
    }
    logger.debug(f"Request parameters: {params}")
    
    try:
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,ru;q=0.5",
            "Connection": "keep-alive",
            "Referer": f"https://data.gov.hk/en-datasets?page={page}&category={category}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.debug(f"Successfully fetched data from {base_url} with params {params}")
        
        data = response.json()
        logger.debug(f"Received JSON response with {data} datasets")

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data from data.gov.hk: {e}")
        return {"error": f"Failed to fetch data from data.gov.hk: {e}"}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {e}"}
