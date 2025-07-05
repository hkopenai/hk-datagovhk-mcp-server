import unittest
from unittest.mock import patch, MagicMock
import requests
from hkopenai.hk_datagovhk_mcp_server.tools.datagovhk_crawler import crawl_datasets

"""
Unit tests for the datagovhk_crawler module.
This module tests the functionality of crawling dataset information from data.gov.hk.
"""

class TestDatagovhkCrawler(unittest.TestCase):
    """Test case class for testing dataset crawling from data.gov.hk."""
    @patch("requests.get")
    def test_crawl_datasets(self, mock_get):
        # Mock the JSON response from data.gov.hk API
        mock_response_json = {
            "datasets": [
                {
                "category": "health",
                "description": {
                    "en": "List showing the product name, trademark text, product holder (pCm wholesaler/ pCm manufacturer), pCm registration number/application number and active ingredients displayed on the pCm label etc.",
                    "sc": "列表显示产品名称，商标文字，注册持有人/申请人，中成药过渡性注册编号(HKP)/中成药注册编号(HKC)及标签显示的有效成分等",
                    "tc": "列表顯示產品名稱，商標文字，註冊持有人/申請人，中成藥過渡性註冊編號(HKP)/中成藥註冊編號(HKC)及標籤顯示的有效成分等"
                },
                "format": [
                    "XML"
                ],
                "id": "hk-dh-cmd-cmd-list-of-proprietary-chinese-medicine",
                "isApiAvailable": "false",
                "name": {
                    "en": "List of applications for proprietary Chinese medicine (pCm) registration",
                    "sc": "中成药名",
                    "tc": "中成藥名單"
                },
                "provider": "hk-dh",
                "score": "null"
                },
                {
                "category": "health",
                "description": {
                    "en": "The dataset contains daily count of COVID-19 vaccination in different age groups",
                    "sc": "数据集附有不同年龄组别每日的2019冠状病毒病疫苗接种数目",
                    "tc": "數據集附有不同年齡組別每日的2019冠狀病毒病疫苗接種數目"
                },
                "format": [
                    "CSV"
                ],
                "id": "hk-hhb-hhbcovid19-vaccination-rates-over-time-by-age",
                "isApiAvailable": "false",
                "name": {
                    "en": "Daily count of vaccination by age groups",
                    "sc": "按年龄组别划分的2019冠状病毒病疫苗接种数目",
                    "tc": "按年齡組別劃分的2019冠狀病毒病疫苗接種數目"
                },
                "provider": "hk-hhb",
                "score": "null"
                }

            ],
            "total": 119
            }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_json
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        category = "city-management"
        page = 1
        result = crawl_datasets(category, page)

        self.assertIn("datasets", result)

    @patch("requests.get")
    def test_crawl_datasets_no_results(self, mock_get):
        mock_response_json = {
            "datasets": [],
            "total": 0
        }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_json
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        category = "nonexistent"
        page = 1
        limit = 12
        offset = (page - 1) * limit
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,ru;q=0.5",
            "Connection": "keep-alive",
            "Referer": f"https://data.gov.hk/en-datasets?page={page}&category={category}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        result = crawl_datasets(category, page)

        mock_get.assert_called_once_with(
            "https://data.gov.hk/api/v1/datasets",
            params={'limit': limit, 'offset': offset, 'category': category, 'lang': 'en'},
            headers=headers,
            timeout=10
        )

        self.assertIn("datasets", result)

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
        """Test handling of general exceptions during dataset crawling."""
        mock_get.side_effect = Exception("Something unexpected happened")

        category = "finance"
        page = 1
        result = crawl_datasets(category, page)

        self.assertIn("error", result)
        self.assertIn("An unexpected error occurred", result["error"])


if __name__ == "__main__":
    unittest.main()
