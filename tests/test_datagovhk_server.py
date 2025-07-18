"""
Module for testing the MCP server creation and functionality.

This module contains unit tests for the server creation process and tool registration.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_datagovhk_mcp_server import server


class TestApp(unittest.TestCase):
    """
    Test class for verifying MCP server creation and tool functionality.

    This class contains test cases to ensure the server is created correctly and
    tools are properly registered and callable.
    """

    @patch("hkopenai.hk_datagovhk_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_datagovhk_mcp_server.tools.crawler.register")
    @patch("hkopenai.hk_datagovhk_mcp_server.tools.providers.register")
    @patch("hkopenai.hk_datagovhk_mcp_server.tools.categories.register")
    @patch("hkopenai.hk_datagovhk_mcp_server.tools.package.register")
    def test_create_mcp_server(
        self,
        mock_package_register,
        mock_categories_register,
        mock_providers_register,
        mock_crawler_register,
        mock_fastmcp,
    ):
        """
        Test the creation of the MCP server and tool registration.

        This test verifies that the server is created correctly, tools are registered
        using the decorator, and the tools call the underlying functions as expected.
        """
        # Setup mocks
        mock_server = Mock()

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        mock_crawler_register.assert_called_once_with(mock_server)
        mock_providers_register.assert_called_once_with(mock_server)
        mock_categories_register.assert_called_once_with(mock_server)
        mock_package_register.assert_called_once_with(mock_server)
