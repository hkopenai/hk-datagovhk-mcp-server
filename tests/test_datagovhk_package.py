"""
Module for testing the datagovhk_package tool.

This module contains unit tests for fetching and processing data.gov.hk package data.
"""

import unittest
from unittest.mock import patch, MagicMock
import requests

from hkopenai.hk_datagovhk_mcp_server.tools.datagovhk_package import _get_package_data
from hkopenai.hk_datagovhk_mcp_server.tools.datagovhk_package import register


class TestDatagovhkPackage(unittest.TestCase):
    """
    Test class for verifying datagovhk_package functionality.

    This class contains test cases to ensure the data fetching and processing
    for data.gov.hk package data work as expected.
    """

    @patch('requests.get')
    def test_get_package_data_success(self, mock_get):
        """
        Test successful fetching of package data.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {"id": "test_id", "name": "Test Package"}}
        mock_get.return_value = mock_response

        result = _get_package_data(package_id="test_id", language="en")
        self.assertIn("result", result)
        self.assertEqual(result["result"]["id"], "test_id")

    @patch('requests.get')
    def test_get_package_data_http_error(self, mock_get):
        """
        Test handling of HTTP errors during package data fetching.
        """
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")
        mock_get.return_value = mock_response

        result = _get_package_data(package_id="test_id", language="en")
        self.assertIn("error", result)
        self.assertIn("Failed to fetch package data", result["error"])

    @patch('requests.get')
    def test_get_package_data_request_exception(self, mock_get):
        """
        Test handling of request exceptions during package data fetching.
        """
        mock_get.side_effect = requests.exceptions.RequestException("Connection Error")

        result = _get_package_data(package_id="test_id", language="en")
        self.assertIn("error", result)
        self.assertIn("Failed to fetch package data", result["error"])

    @patch('requests.get')
    def test_get_package_data_unexpected_error(self, mock_get):
        """
        Test handling of unexpected errors during package data fetching.
        """
        mock_get.side_effect = Exception("Unexpected Error")

        result = _get_package_data(package_id="test_id", language="en")
        self.assertIn("error", result)
        self.assertIn("Failed to fetch package data", result["error"])

    def test_register_tool(self):
        """
        Test the registration of the get_package_data tool.
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
            "hkopenai.hk_datagovhk_mcp_server.tools.datagovhk_package._get_package_data"
        ) as mock_get_package_data:
            decorated_function(package_id="test_id", language="en")
            mock_get_package_data.assert_called_once_with("test_id", "en")