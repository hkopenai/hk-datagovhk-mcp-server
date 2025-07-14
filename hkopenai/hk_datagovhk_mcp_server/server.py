"""
HK Data.gov.hk MCP Server implementation.

This module provides the core functionality for the MCP server, including tools to interact
with the data.gov.hk API for crawling datasets, fetching providers, categories, and package data.
"""

from fastmcp import FastMCP
from .tools import datagovhk_crawler
from .tools import datagovhk_providers
from .tools import datagovhk_categories
from .tools import datagovhk_package

def server():
    """Create and configure the HK Data.gov.hk MCP server."""
    mcp = FastMCP(name="HKDataGovHKServer")

    datagovhk_crawler.register(mcp)
    datagovhk_providers.register(mcp)
    datagovhk_categories.register(mcp)
    datagovhk_package.register(mcp)

    return mcp
