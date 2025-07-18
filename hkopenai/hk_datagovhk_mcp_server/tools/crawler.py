"""
Crawl datasets from data.gov.hk API.

This module retrieves dataset info from data.gov.hk by category and page.
"""

import logging
from typing import Dict, Any
from hkopenai_common.json_utils import fetch_json_data
from pydantic import Field
from typing_extensions import Annotated

# Configure logging
logger = logging.getLogger(__name__)


def register(mcp):
    """Registers the datagovhk_crawler tool with the FastMCP server."""

    @mcp.tool(
        description="Crawl datasets from data.gov.hk based on category and page.",
    )
    def crawl_datasets(
        category: Annotated[str, Field(description="The category to filter datasets.")],
        page: Annotated[
            int, Field(description="The page number to retrieve (default is 1).")
        ] = 1,
    ) -> Dict:
        """Crawl datasets from data.gov.hk for a given category and page number.

        Args:
            category: The category to filter datasets.
            page: The page number to retrieve (default is 1).

        Returns:
            A dictionary containing the crawled dataset information.
        """
        return _crawl_datasets(category, page)


def _crawl_datasets(category: str, page: int = 1) -> Dict[str, Any]:
    """
    Crawl datasets from data.gov.hk based on category and page number using API.

    Args:
        category: The category of datasets to crawl (e.g., 'city-management').
        page: The page number to crawl (default: 1).

    Returns:
        Dict containing a list of datasets with their titles and links.
    """
    logger.debug("Starting crawl for category: %s, page: %d", category, page)
    base_url = "https://data.gov.hk/api/v1/datasets"
    limit = 12
    offset = (page - 1) * limit
    params = {"limit": limit, "offset": offset, "category": category, "lang": "en"}
    logger.debug("Request parameters: %s", params)
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,ru;q=0.5",
        "Connection": "keep-alive",
        "Referer": f"https://data.gov.hk/en-datasets?page={page}&category={category}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": (
            r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            r"(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        ),
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": (
            r"\"Not)A;Brand\"\;v=\"8\", \"Chromium\"\;v=\"138\", "
            r"\"Microsoft Edge\"\;v=\"138\""
        ),
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": r"\"Windows\"",
    }
    data = fetch_json_data(base_url, params=params, headers=headers, timeout=10)
    logger.debug("Received JSON response with %s datasets", len(data.get("data", [])))

    return data
