"""
Module for testing the datagovhk_crawler tool.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_datagovhk_mcp_server.tools.crawler import _crawl_datasets
from hkopenai.hk_datagovhk_mcp_server.tools.crawler import register


class TestDatagovhkCrawler(unittest.TestCase):
    """
    Test class for verifying datagovhk_crawler functionality.

    This class contains test cases to ensure the data fetching and processing
    for data.gov.hk datasets work as expected.
    """

    @patch("hkopenai.hk_datagovhk_mcp_server.tools.crawler.fetch_json_data")
    def test_crawl_datasets_success(self, mock_fetch_json_data):
        """Happy path: tool returns the dict produced by fetch_json_data."""
        mock_fetch_json_data.return_value = {
            "data": [
                {"title": "Dataset 1", "link": "link1"},
                {"title": "Dataset 2", "link": "link2"},
            ]
        }

        result = _crawl_datasets(category="test", page=1)
        self.assertIn("data", result)
        self.assertEqual(len(result["data"]), 2)
        self.assertEqual(result["data"][0]["title"], "Dataset 1")

    @patch("hkopenai.hk_datagovhk_mcp_server.tools.crawler.fetch_json_data")
    def test_crawl_datasets_http_error(self, mock_fetch_json_data):
        """
        Test handling of HTTP errors during crawling.

        fetch_json_data converts HTTP errors (4xx/5xx) into {"error": ...}
        dicts before returning. The tool surfaces the dict verbatim.
        """
        mock_fetch_json_data.return_value = {"error": "HTTP error occurred: 500"}

        result = _crawl_datasets(category="test", page=1)
        self.assertIn("error", result)
        self.assertIn("HTTP error occurred", result["error"])

    @patch("hkopenai.hk_datagovhk_mcp_server.tools.crawler.fetch_json_data")
    def test_crawl_datasets_request_exception(self, mock_fetch_json_data):
        """
        Test handling of request exceptions during crawling.

        fetch_json_data converts connection errors into {"error": ...}
        dicts before returning.
        """
        mock_fetch_json_data.return_value = {"error": "Connection error occurred"}

        result = _crawl_datasets(category="test", page=1)
        self.assertIn("error", result)
        self.assertIn("Connection error occurred", result["error"])

    @patch("hkopenai.hk_datagovhk_mcp_server.tools.crawler.fetch_json_data")
    def test_crawl_datasets_unexpected_error(self, mock_fetch_json_data):
        """
        Test handling of unexpected errors during crawling.

        fetch_json_data wraps any unhandled exception into
        {"error": "An unexpected error occurred during the request: ..."}.
        """
        mock_fetch_json_data.return_value = {
            "error": "An unexpected error occurred during the request: Boom"
        }

        result = _crawl_datasets(category="test", page=1)
        self.assertIn("error", result)
        self.assertIn("An unexpected error occurred", result["error"])

    def test_register_tool(self):
        """
        Test the registration of the crawl_datasets tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _crawl_datasets function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Crawl datasets from data.gov.hk based on category and page.",
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "crawl_datasets")

        # Call the decorated function and verify it calls _crawl_datasets
        with patch(
            "hkopenai.hk_datagovhk_mcp_server.tools.crawler._crawl_datasets"
        ) as mock_crawl_datasets:
            decorated_function(category="test_cat", page=2)
            mock_crawl_datasets.assert_called_once_with("test_cat", 2)
