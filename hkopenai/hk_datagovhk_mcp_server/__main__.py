"""
Main entry point for the HK Data.gov.hk MCP Server.

This script serves as the command-line interface to start the MCP server with configurable options.
"""



from hkopenai_common.cli_utils import cli_main
from .server import server

if __name__ == "__main__":
    cli_main(server, "HK Datagovhk MCP Server")
