"""
Module for testing the datagovhk_crawler tool.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_datagovhk_mcp_server.tools.crawler import _crawl_datasets
from hkopenai.hk_datagovhk_mcp_server.tools.crawler import register
from hkopenai_common.json_utils import fetch_json_data
from hkopenai_common.json_utils import fetch_json_data
from hkopenai_common.json_utils import fetch_json_data
from hkopenai_common.json_utils import fetch_json_data


class TestDatagovhkCrawler(unittest.TestCase):
    """
    Test class for verifying datagovhk_crawler functionality.

    This class contains test cases to ensure the data fetching and processing
    for data.gov.hk datasets work as expected.
    """

    @patch("requests.get")
    def test_crawl_datasets_success(self, mock_get):
        """
        Test successful crawling of datasets.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"title": "Dataset 1", "link": "link1"},
                {"title": "Dataset 2", "link": "link2"},
            ]
        }
        mock_get.return_value = mock_response

        result = _crawl_datasets(category="test", page=1)
        self.assertIn("data", result)
        self.assertEqual(len(result["data"]), 2)
        self.assertEqual(result["data"][0]["title"], "Dataset 1")

    @patch("requests.get")
    def test_crawl_datasets_http_error(self, mock_get):
        """
        Test handling of HTTP errors during crawling.
        """
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Not Found"
        )
        mock_get.return_value = mock_response

        result = _crawl_datasets(category="test", page=1)
        self.assertIn("error", result)
        self.assertIn("Failed to fetch data", result["error"])

    @patch("requests.get")
    def test_crawl_datasets_request_exception(self, mock_get):
        """
        Test handling of request exceptions during crawling.
        """
        mock_get.side_effect = requests.exceptions.RequestException("Connection Error")

        result = _crawl_datasets(category="test", page=1)
        self.assertIn("error", result)
        self.assertIn("Failed to fetch data", result["error"])

    @patch("hkopenai_common.json_utils.fetch_json_data")
    def test_crawl_datasets_unexpected_error(self, mock_fetch_json_data):
        """
        Test handling of unexpected errors during crawling.
        """
        mock_fetch_json_data.side_effect = Exception("An unexpected error occurred")

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
