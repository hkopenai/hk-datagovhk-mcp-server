"""
Module for testing the datagovhk_providers tool.
"""

import unittest
from unittest.mock import patch, MagicMock


from hkopenai.hk_datagovhk_mcp_server.tools.providers import _get_providers
from hkopenai.hk_datagovhk_mcp_server.tools.providers import register


class TestDatagovhkProviders(unittest.TestCase):
    """
    Test class for verifying datagovhk_providers functionality.

    This class contains test cases to ensure the data fetching and processing
    for data.gov.hk providers work as expected.
    """

    @patch("hkopenai_common.json_utils.fetch_json_data")
    def test_get_providers_unexpected_error(self, mock_fetch_json_data):
        """
        Test handling of unexpected errors during provider fetching.
        """
        mock_fetch_json_data.side_effect = Exception("An unexpected error occurred")

        result = _get_providers(language="en")
        self.assertIn("error", result)
        self.assertIn("An unexpected error occurred", result["error"])

    def test_register_tool(self):
        """
        Test the registration of the get_providers tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_providers function.
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
