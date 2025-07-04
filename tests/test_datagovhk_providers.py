import unittest
from unittest.mock import patch, MagicMock
import requests
from hkopenai.hk_datagovhk_mcp_server.tools.datagovhk_providers import get_providers

class TestDatagovhkProviders(unittest.TestCase):
    @patch("requests.get")
    def test_get_providers_success_en(self, mock_get):
        # Mock the JSON response from data.gov.hk for English providers
        mock_response_json = {
            "providers": [
                {
                    "datasetCount": 12,
                    "id": "hk-aw",
                    "name": {
                        "en": "Administration Wing, Chief Secretary for Administration's Office",
                        "sc": "政务司司长办公室辖下行政署",
                        "tc": "政務司司長辦公室轄下行政署"
                    }
                },
                {
                    "datasetCount": 52,
                    "id": "hk-afcd",
                    "name": {
                        "en": "Agriculture, Fisheries and Conservation Department",
                        "sc": "渔农自然护理署",
                        "tc": "漁農自然護理署"
                    }
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_json
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_providers("en")

        mock_get.assert_called_once_with(
            "https://data.gov.hk/filestore/json/providers_en.json",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )
        self.assertIn("providers", result)
        self.assertEqual(len(result["providers"]), 2)

    @patch("requests.get")
    def test_get_providers_success_tc(self, mock_get):
        # Mock the JSON response from data.gov.hk for Traditional Chinese providers
        mock_response_json = {
            "providers": [
                {
                    "datasetCount": 12,
                    "id": "hk-aw",
                    "name": {
                        "en": "Administration Wing, Chief Secretary for Administration's Office",
                        "sc": "政务司司长办公室辖下行政署",
                        "tc": "政務司司長辦公室轄下行政署"
                    }
                },
                {
                    "datasetCount": 52,
                    "id": "hk-afcd",
                    "name": {
                        "en": "Agriculture, Fisheries and Conservation Department",
                        "sc": "渔农自然护理署",
                        "tc": "漁農自然護理署"
                    }
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_json
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_providers("tc")

        mock_get.assert_called_once_with(
            "https://data.gov.hk/filestore/json/providers_tc.json",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )
        self.assertIn("providers", result)
        self.assertEqual(len(result["providers"]), 2)

    @patch("requests.get")
    def test_get_providers_success_sc(self, mock_get):
        # Mock the JSON response from data.gov.hk for Simplified Chinese providers
        mock_response_json = {
            "providers": [
                {
                    "datasetCount": 12,
                    "id": "hk-aw",
                    "name": {
                        "en": "Administration Wing, Chief Secretary for Administration's Office",
                        "sc": "政务司司长办公室辖下行政署",
                        "tc": "政務司司長辦公室轄下行政署"
                    }
                },
                {
                    "datasetCount": 52,
                    "id": "hk-afcd",
                    "name": {
                        "en": "Agriculture, Fisheries and Conservation Department",
                        "sc": "渔农自然护理署",
                        "tc": "漁農自然護理署"
                    }
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_json
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_providers("sc")

        mock_get.assert_called_once_with(
            "https://data.gov.hk/filestore/json/providers_sc.json",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )
        self.assertIn("providers", result)
        self.assertEqual(len(result["providers"]), 2)

    @patch("requests.get")
    def test_get_providers_default_language(self, mock_get):
        # Mock the JSON response from data.gov.hk for default (English) providers
        mock_response_json = {
            "providers": [
                {
                    "datasetCount": 12,
                    "id": "hk-aw",
                    "name": {
                        "en": "Administration Wing, Chief Secretary for Administration's Office",
                        "sc": "政务司司长办公室辖下行政署",
                        "tc": "政務司司長辦公室轄下行政署"
                    }
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_json
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_providers("invalid_language")

        mock_get.assert_called_once_with(
            "https://data.gov.hk/filestore/json/providers_en.json",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )
        self.assertIn("providers", result)

    @patch("requests.get")
    def test_get_providers_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        result = get_providers("en")

        self.assertIn("error", result)
        self.assertIn("Failed to fetch providers data", result["error"])

    @patch("requests.get")
    def test_get_providers_general_exception(self, mock_get):
        mock_get.side_effect = Exception("Something unexpected happened")

        result = get_providers("en")

        self.assertIn("error", result)
        self.assertIn("An unexpected error occurred", result["error"])

if __name__ == "__main__":
    unittest.main()
