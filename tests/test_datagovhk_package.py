"""
Module for testing the datagovhk_package tool.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_datagovhk_mcp_server.tools.package import _get_package_data
from hkopenai.hk_datagovhk_mcp_server.tools.package import register


class TestDatagovhkPackage(unittest.TestCase):
    """
    Test class for verifying datagovhk_package functionality.

    This class contains test cases to ensure the data fetching and processing
    for data.gov.hk package data work as expected.
    """

    @patch("hkopenai.hk_datagovhk_mcp_server.tools.package.fetch_json_data")
    def test_get_package_data_success(self, mock_fetch_json_data):
        """Happy path: tool returns the dict produced by fetch_json_data."""
        mock_fetch_json_data.return_value = {
            "result": {"id": "test_id", "name": "Test Package"}
        }

        result = _get_package_data(package_id="test_id", language="en")
        self.assertIn("result", result)
        self.assertEqual(result["result"]["id"], "test_id")

    @patch("hkopenai.hk_datagovhk_mcp_server.tools.package.fetch_json_data")
    def test_get_package_data_http_error(self, mock_fetch_json_data):
        """
        Test handling of HTTP errors during package data fetching.

        fetch_json_data converts HTTP errors (4xx/5xx) into {"error": ...}
        dicts before returning. The tool surfaces the dict verbatim.
        """
        mock_fetch_json_data.return_value = {"error": "HTTP error occurred: 404"}

        result = _get_package_data(package_id="test_id", language="en")
        self.assertIn("error", result)
        self.assertIn("HTTP error occurred", result["error"])

    @patch("hkopenai.hk_datagovhk_mcp_server.tools.package.fetch_json_data")
    def test_get_package_data_request_exception(self, mock_fetch_json_data):
        """
        Test handling of request exceptions during package data fetching.

        fetch_json_data converts connection errors into {"error": ...}
        dicts before returning.
        """
        mock_fetch_json_data.return_value = {"error": "Connection error occurred"}

        result = _get_package_data(package_id="test_id", language="en")
        self.assertIn("error", result)
        self.assertIn("Connection error occurred", result["error"])

    @patch("hkopenai.hk_datagovhk_mcp_server.tools.package.fetch_json_data")
    def test_get_package_data_unexpected_error(self, mock_fetch_json_data):
        """
        Test handling of unexpected errors during package data fetching.

        fetch_json_data wraps any unhandled exception into
        {"error": "An unexpected error occurred during the request: ..."}.
        """
        mock_fetch_json_data.return_value = {
            "error": "An unexpected error occurred during the request: Boom"
        }

        result = _get_package_data(package_id="test_id", language="en")
        self.assertIn("error", result)
        self.assertIn("An unexpected error occurred", result["error"])

    def test_register_tool(self):
        """
        Test the registration of the get_package_data tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_package_data function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description=(
                "Fetch package data from data.gov.hk API using the provided ID and language, "
                "typically obtained from the crawler tool."
            ),
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_package_data")

        # Call the decorated function and verify it calls _get_package_data
        with patch(
            "hkopenai.hk_datagovhk_mcp_server.tools.package._get_package_data"
        ) as mock_get_package_data:
            decorated_function(package_id="test_id", language="en")
            mock_get_package_data.assert_called_once_with("test_id", "en")
