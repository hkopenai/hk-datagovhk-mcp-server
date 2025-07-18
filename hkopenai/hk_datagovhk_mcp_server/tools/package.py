"""
Fetch package data from data.gov.hk API.

This module retrieves detailed package info from data.gov.hk using package IDs.
"""

import logging
from typing import Dict, Any
from hkopenai_common.json_utils import fetch_json_data
from pydantic import Field
from typing_extensions import Annotated

# Configure logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def register(mcp):
    """Registers the datagovhk_package tool with the FastMCP server."""

    @mcp.tool(
        description=(
            "Fetch package data from data.gov.hk API using the provided ID and language, "
            "typically obtained from the crawler tool."
        ),
    )
    def get_package_data(
        package_id: Annotated[
            str, Field(description="The unique identifier of the package to retrieve.")
        ],
        language: Annotated[
            str,
            Field(
                description="The language code (en, tc, sc) for the data (default is 'en')."
            ),
        ] = "en",
    ) -> Dict:
        """Fetch detailed package data from data.gov.hk using the package ID.

        Args:
            package_id: The unique identifier of the package to retrieve.
            language: The language code (en, tc, sc) for the data (default is 'en').

        Returns:
            A dictionary containing the detailed package information.
        """
        return _get_package_data(package_id, language)


def _get_package_data(package_id: str, language: str = "en") -> Dict[str, Any]:
    """
    Fetch package data from data.gov.hk API using the provided ID and language.

    Args:
        package_id: The ID of the package to fetch data for.
        language: The language code (en, tc, sc) to fetch the data in. Defaults to "en".

    Returns:
        Dict containing the package data.
    """
    logger.debug(
        "Fetching package data for ID: %s in language: %s", package_id, language
    )
    if language not in ["en", "tc", "sc"]:
        logger.error("Invalid language code: %s. Defaulting to 'en'.", language)
        language = "en"
    url = (
        f"https://data.gov.hk/{language}-data/api/3/action/package_show?id={package_id}"
    )
    logger.debug("Using URL: %s", url)
    headers = {
        "Accept": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
        ),
    }
    return fetch_json_data(url, headers=headers, timeout=10)
