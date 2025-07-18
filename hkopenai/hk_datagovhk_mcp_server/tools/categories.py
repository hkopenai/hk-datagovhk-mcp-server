"""
Fetch dataset categories from data.gov.hk API.

This module retrieves category data from data.gov.hk in various languages.
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
    """Registers the datagovhk_categories tool with the FastMCP server."""

    @mcp.tool(
        description="Fetch categories from data.gov.hk based on language (en, tc, sc).",
    )
    def get_categories(
        language: Annotated[
            str,
            Field(
                description="The language code (en, tc, sc) for the data (default is 'en')."
            ),
        ] = "en",
    ) -> Dict:
        """Fetch dataset categories from data.gov.hk in the specified language.

        Args:
            language: The language code (en, tc, sc) for the data (default is 'en').

        Returns:
            A dictionary containing the list of categories.
        """
        return _get_categories(language)


def _get_categories(language: str = "en") -> Dict[str, Any]:
    """
    Fetch categories from data.gov.hk based on the specified language.

    Args:
        language: The language code for the categories list (en, tc, sc). Defaults to 'en'.

    Returns:
        Dict containing the categories data.
    """
    logger.debug("Fetching categories for language: %s", language)
    url_map = {
        "en": "https://data.gov.hk/filestore/json/categories_en.json",
        "tc": "https://data.gov.hk/filestore/json/categories_tc.json",
        "sc": "https://data.gov.hk/filestore/json/categories_sc.json",
    }
    url = url_map.get(language, url_map["en"])
    logger.debug("Using URL: %s", url)
    return fetch_json_data(url)
