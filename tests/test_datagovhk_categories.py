import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_datagovhk_mcp_server.tools.datagovhk_categories import get_categories

class TestDataGovHKCategories(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "categories": [
                {
                    "id": "city-management",
                    "name": {
                        "en": "City Management and Utilities",
                        "tc": "城市管理及公共設施",
                        "sc": "城市管理及公共设施"
                    }
                },
                {
                    "id": "climate-and-weather",
                    "name": {
                        "en": "Climate and Weather",
                        "tc": "氣象",
                        "sc": "气象"
                    }
                }
            ]
        }

    @patch('requests.get')
    def test_get_categories_en(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_categories(language="en")
        self.assertEqual(result, self.sample_data)
        mock_get.assert_called_once_with(
            "https://data.gov.hk/filestore/json/categories_en.json",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )

    @patch('requests.get')
    def test_get_categories_tc(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_categories(language="tc")
        self.assertEqual(result, self.sample_data)
        mock_get.assert_called_once_with(
            "https://data.gov.hk/filestore/json/categories_tc.json",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )

    @patch('requests.get')
    def test_get_categories_sc(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_categories(language="sc")
        self.assertEqual(result, self.sample_data)
        mock_get.assert_called_once_with(
            "https://data.gov.hk/filestore/json/categories_sc.json",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )

    @patch('requests.get')
    def test_get_categories_invalid_language(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_categories(language="invalid")
        self.assertEqual(result, self.sample_data)
        mock_get.assert_called_once_with(
            "https://data.gov.hk/filestore/json/categories_en.json",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )

    @patch('requests.get')
    def test_get_categories_request_exception(self, mock_get):
        mock_get.side_effect = Exception("Request failed")

        result = get_categories(language="en")
        self.assertIn("error", result)
        self.assertIn("Request failed", result["error"])

if __name__ == '__main__':
    unittest.main()
