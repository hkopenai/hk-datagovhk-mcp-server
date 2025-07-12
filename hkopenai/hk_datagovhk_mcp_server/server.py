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

def create_mcp_server():
    """Create and configure the HK Data.gov.hk MCP server."""
    mcp = FastMCP(name="HKDataGovHKServer")

    datagovhk_crawler.register(mcp)
    datagovhk_providers.register(mcp)
    datagovhk_categories.register(mcp)
    datagovhk_package.register(mcp)

    return mcp

def main(args):
    """Main function to start the HK Data.gov.hk MCP Server with command-line arguments.
    
    Args:
        args: Parsed command-line arguments.
    """
    server = create_mcp_server()
    if args.sse:
        server.run(transport="streamable-http", host=args.host, port=args.port)
        print(f"HK Data.gov.hk MCP Server running in SSE mode on port {args.port}, bound to {args.host}")
    else:
        server.run()
        print("HK Data.gov.hk MCP Server running in stdio mode")
