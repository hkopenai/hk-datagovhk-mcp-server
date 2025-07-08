"""
HK Data.gov.hk MCP Server implementation.

This module provides the core functionality for the MCP server, including tools to interact
with the data.gov.hk API for crawling datasets, fetching providers, categories, and package data.
"""

import argparse
from typing import Dict
from fastmcp import FastMCP
from .tools import datagovhk_crawler
from .tools import datagovhk_providers
from .tools import datagovhk_categories
from .tools import datagovhk_package

def create_mcp_server():
    """Create and configure the HK Data.gov.hk MCP server."""
    mcp = FastMCP(name="HKDataGovHKServer")

    @mcp.tool(
        description="Crawl datasets from data.gov.hk based on category and page.",
    )
    def crawl_datasets(category: str, page: int = 1) -> Dict:
        """Crawl datasets from data.gov.hk for a given category and page number.
        
        Args:
            category: The category to filter datasets.
            page: The page number to retrieve (default is 1).
            
        Returns:
            A dictionary containing the crawled dataset information.
        """
        return datagovhk_crawler.crawl_datasets(category, page)

    @mcp.tool(
        description="Fetch providers from data.gov.hk based on language (en, tc, sc).",
    )
    def get_providers(language: str = "en") -> Dict:
        """Fetch data providers from data.gov.hk in the specified language.
        
        Args:
            language: The language code (en, tc, sc) for the data (default is 'en').
            
        Returns:
            A dictionary containing the list of providers.
        """
        return datagovhk_providers.get_providers(language)

    @mcp.tool(
        description="Fetch categories from data.gov.hk based on language (en, tc, sc).",
    )
    def get_categories(language: str = "en") -> Dict:
        """Fetch dataset categories from data.gov.hk in the specified language.
        
        Args:
            language: The language code (en, tc, sc) for the data (default is 'en').
            
        Returns:
            A dictionary containing the list of categories.
        """
        return datagovhk_categories.get_categories(language)

    @mcp.tool(
        description=(
            "Fetch package data from data.gov.hk API using the provided ID and language, "
            "typically obtained from the crawler tool."
        ),
    )
    def get_package_data(package_id: str, language: str = "en") -> Dict:
        """Fetch detailed package data from data.gov.hk using the package ID.
        
        Args:
            package_id: The unique identifier of the package to retrieve.
            language: The language code (en, tc, sc) for the data (default is 'en').
            
        Returns:
            A dictionary containing the detailed package information.
        """
        return datagovhk_package.get_package_data(package_id, language)
    return mcp

def main(args):
    """Main function to start the HK Data.gov.hk MCP Server with command-line arguments.
    
    Args:
        args: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='HK Data.gov.hk MCP Server')
    parser.add_argument('-s', '--sse', action='store_true',
                       help='Run in SSE mode instead of stdio')
    parser.add_argument('-p', '--port', type=int, default=8000,
                       help='Port to run the server on (default: 8000)')
    parser.add_argument('--host', type=str, default="127.0.0.1", 
                       help='Host to bind the server to')
    args = parser.parse_args()

    print(f"[DEBUG] Parsed arguments: {args}")
    server = create_mcp_server()
    if args.sse:
        server.run(transport="streamable-http", host=args.host, port=args.port)
        print(f"HK Data.gov.hk MCP Server running in SSE mode on port {args.port}, bound to {args.host}")
    else:
        server.run()
        print("HK Data.gov.hk MCP Server running in stdio mode")
