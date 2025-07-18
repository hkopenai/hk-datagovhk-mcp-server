"""
HK Data.gov.hk MCP Server implementation.

This module provides the core functionality for the MCP server, including tools to interact
with the data.gov.hk API for crawling datasets, fetching providers, categories, and package data.
"""

from fastmcp import FastMCP
from .tools import crawler
from .tools import providers
from .tools import categories
from .tools import package


def server():
    """Create and configure the HK Data.gov.hk MCP server."""
    mcp = FastMCP(name="HKDataGovHKServer")

    crawler.register(mcp)
    providers.register(mcp)
    categories.register(mcp)
    package.register(mcp)

    return mcp
