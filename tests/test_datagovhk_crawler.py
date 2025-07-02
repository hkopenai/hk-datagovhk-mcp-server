import unittest
from unittest.mock import patch, MagicMock
import requests
from hkopenai.hk_datagovhk_mcp_server.tools.datagovhk_crawler import crawl_datasets

class TestDatagovhkCrawler(unittest.TestCase):
    @patch("requests.get")
    def test_crawl_datasets(self, mock_get):
        # Mock the response from data.gov.hk
        mock_response_content = '''
        <div class="dataset-item">
            <h3 class="dataset-title"><a href="/en-datasets/dataset1">Dataset 1 Title</a></h3>
            <a class="dataset-link" href="https://data.gov.hk/en-datasets/dataset1">Link 1</a>
        </div>
        <div class="dataset-item">
            <h3 class="dataset-title"><a href="/en-datasets/dataset2">Dataset 2 Title</a></h3>
            <a class="dataset-link" href="https://data.gov.hk/en-datasets/dataset2">Link 2</a>
        </div>
        '''
        mock_response = MagicMock()
        mock_response.text = mock_response_content
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        category = "finance"
        page = 1
        result = crawl_datasets(category, page)

        mock_get.assert_called_once_with(
            "https://data.gov.hk/en-datasets", params={'page': page, 'category': category}
        )

        self.assertIn("category", result)
        self.assertEqual(result["category"], category)
        self.assertIn("page", result)
        self.assertEqual(result["page"], page)
        self.assertIn("datasets", result)
        self.assertEqual(len(result["datasets"]), 2)
        self.assertEqual(result["datasets"][0]["title"], "Dataset 1 Title")
        self.assertEqual(result["datasets"][0]["link"], "https://data.gov.hk/en-datasets/dataset1")
        self.assertEqual(result["datasets"][1]["title"], "Dataset 2 Title")
        self.assertEqual(result["datasets"][1]["link"], "https://data.gov.hk/en-datasets/dataset2")

    @patch("requests.get")
    def test_crawl_datasets_no_results(self, mock_get):
        mock_response_content = '''
        <div>No datasets found</div>
        '''
        mock_response = MagicMock()
        mock_response.text = mock_response_content
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        category = "nonexistent"
        page = 1
        result = crawl_datasets(category, page)

        self.assertEqual(len(result["datasets"]), 0)

    @patch("requests.get")
    def test_crawl_datasets_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        category = "finance"
        page = 1
        result = crawl_datasets(category, page)

        self.assertIn("error", result)
        self.assertIn("Failed to fetch data", result["error"])

    @patch("requests.get")
    def test_crawl_datasets_general_exception(self, mock_get):
        mock_get.side_effect = Exception("Something unexpected happened")

        category = "finance"
        page = 1
        result = crawl_datasets(category, page)

        self.assertIn("error", result)
        self.assertIn("An unexpected error occurred", result["error"])

if __name__ == "__main__":
    unittest.main()
