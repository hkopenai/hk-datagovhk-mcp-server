"""
Main entry point for the HK Data.gov.hk MCP Server.

This script serves as the command-line interface to start the MCP server with configurable options.
"""

import argparse
from .server import main as server_main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HK Data.gov.hk MCP Server')
    parser.add_argument('-s', '--sse', action='store_true',
                       help='Run in SSE mode instead of stdio')
    parser.add_argument('-p', '--port', type=int, default=8000,
                       help='Port to run the server on (default: 8000)')
    args = parser.parse_args()
    server_main(args)
