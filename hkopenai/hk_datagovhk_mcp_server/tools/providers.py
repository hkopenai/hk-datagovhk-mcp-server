"""
Fetch providers from data.gov.hk API.

This module retrieves provider info from data.gov.hk in various languages.
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
    """Registers the datagovhk_providers tool with the FastMCP server."""

    @mcp.tool(
        description="Fetch providers from data.gov.hk based on language (en, tc, sc).",
    )
    def get_providers(
        language: Annotated[
            str,
            Field(
                description="The language code (en, tc, sc) for the data (default is 'en')."
            ),
        ] = "en",
    ) -> Dict:
        """Fetch data providers from data.gov.hk in the specified language.

        Args:
            language: The language code (en, tc, sc) for the data (default is 'en').

        Returns:
            A dictionary containing the list of providers.
        """
        return _get_providers(language)


def _get_providers(language: str = "en") -> Dict[str, Any]:
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
        "sc": "https://data.gov.hk/filestore/json/providers_sc.json",
    }
    url = url_map.get(language, url_map["en"])
    logger.debug("Using URL: %s", url)
    headers = {
        "Accept": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/* Safari/* Edg/*"
        ),
    }
    return fetch_json_data(url, headers=headers, timeout=10)
