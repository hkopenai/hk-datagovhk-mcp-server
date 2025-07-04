import argparse
from fastmcp import FastMCP
from typing import Dict, Annotated, Optional
from pydantic import Field
from hkopenai.hk_datagovhk_mcp_server.tools import datagovhk_crawler, datagovhk_providers, datagovhk_categories, datagovhk_api

def create_mcp_server():
    """Create and configure the HK Data.gov.hk MCP server"""
    mcp = FastMCP(name="HKDataGovHKServer")

    @mcp.tool(
        description="Crawl datasets from data.gov.hk based on category and page number.",
    )
    def crawl_datasets(category: str, page: int = 1) -> Dict:
        return datagovhk_crawler.crawl_datasets(category, page)

    @mcp.tool(
        description="Fetch providers from data.gov.hk based on the specified language (en, tc, sc).",
    )
    def get_providers(language: str = "en") -> Dict:
        return datagovhk_providers.get_providers(language)

    @mcp.tool(
        description="Fetch categories from data.gov.hk based on the specified language (en, tc, sc).",
    )
    def get_categories(language: str = "en") -> Dict:
        return datagovhk_categories.get_categories(language)

    @mcp.tool(
        description="Fetch package data from data.gov.hk API using the provided ID and language, typically obtained from the crawler tool.",
    )
    def get_package_data(id: str, language: str = "en") -> Dict:
        return datagovhk_api.get_package_data(id, language)
    
    return mcp

def main(args):
    parser = argparse.ArgumentParser(description='HK Data.gov.hk MCP Server')
    parser.add_argument('-s', '--sse', action='store_true',
                       help='Run in SSE mode instead of stdio')
    parser.add_argument('-p', '--port', type=int, default=8000,
                       help='Port to run the server on (default: 8000)')
    args = parser.parse_args()

    print(f"[DEBUG] Parsed arguments: {args}")
    server = create_mcp_server()
    
    if args.sse:
        server.run(transport="streamable-http", port=args.port)
        print(f"HK Data.gov.hk MCP Server running in SSE mode on port {args.port}")
    else:
        server.run()
        print("HK Data.gov.hk MCP Server running in stdio mode")
