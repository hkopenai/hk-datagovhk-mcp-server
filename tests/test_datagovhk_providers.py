"""
Module for testing the datagovhk_providers tool.

This module contains unit tests for fetching and processing data.gov.hk providers.
"""

import unittest
from unittest.mock import patch, MagicMock
import requests

from hkopenai.hk_datagovhk_mcp_server.tools.datagovhk_providers import _get_providers
from hkopenai.hk_datagovhk_mcp_server.tools.datagovhk_providers import register


class TestDatagovhkProviders(unittest.TestCase):
    """
    Test class for verifying datagovhk_providers functionality.

    This class contains test cases to ensure the data fetching and processing
    for data.gov.hk providers work as expected.
    """

    @patch('requests.get')
    def test_get_providers_success(self, mock_get):
        """
        Test successful fetching of providers.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"providers": ["Provider1", "Provider2"]}
        mock_get.return_value = mock_response

        result = _get_providers(language="en")
        self.assertIn("providers", result)
        self.assertEqual(len(result["providers"]), 2)
        self.assertEqual(result["providers"][0], "Provider1")

    @patch('requests.get')
    def test_get_providers_http_error(self, mock_get):
        """
        Test handling of HTTP errors during provider fetching.
        """
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")
        mock_get.return_value = mock_response

        result = _get_providers(language="en")
        self.assertIn("error", result)
        self.assertIn("Failed to fetch providers data", result["error"])

    @patch('requests.get')
    def test_get_providers_request_exception(self, mock_get):
        """
        Test handling of request exceptions during provider fetching.
        """
        mock_get.side_effect = requests.exceptions.RequestException("Connection Error")

        result = _get_providers(language="en")
        self.assertIn("error", result)
        self.assertIn("Failed to fetch providers data", result["error"])

    @patch('requests.get')
    def test_get_providers_unexpected_error(self, mock_get):
        """
        Test handling of unexpected errors during provider fetching.
        """
        mock_get.side_effect = Exception("Unexpected Error")

        result = _get_providers(language="en")
        self.assertIn("error", result)
        self.assertIn("An unexpected error occurred", result["error"])

    def test_register_tool(self):
        """
        Test the registration of the get_providers tool.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Fetch providers from data.gov.hk based on language (en, tc, sc).",
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_providers")

        # Call the decorated function and verify it calls _get_providers
        with patch(
            "hkopenai.hk_datagovhk_mcp_server.tools.datagovhk_providers._get_providers"
        ) as mock_get_providers:
            decorated_function(language="en")
            mock_get_providers.assert_called_once_with("en")