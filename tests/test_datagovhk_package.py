import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_datagovhk_mcp_server.tools.datagovhk_package import get_package_data

class TestDataGovHKApi(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "help": "https://data.gov.hk/en-data/api/3/action/help_show?name=package_show",
            "success": True,
            "result": {
                "author": None,
                "author_email": None,
                "creator_user_id": "77dc1126-bc02-45e6-a89b-bf2c5ae85737",
                "data_dictionary": "https://plis.hyd.gov.hk/datagovhk/plis/Data_Specification_for_PLIS_PSI_EN.pdf",
                "id": "770755cb-2a71-4d85-bff3-6b183dea3129",
                "isopen": False,
                "license_id": None,
                "license_title": None,
                "maintainer": "General Enquiries",
                "maintainer_email": "e3-1.ltg@hyd.gov.hk",
                "maintainer_phone": "3903 6567",
                "metadata_created": "2021-07-02T05:48:58.212917",
                "metadata_modified": "2025-06-24T16:32:03.988327",
                "name": "hk-hyd-plis-lamppostdata",
                "notes": "The data provides location information of public lighting lamp posts maintained by Highways Department. The multiple file formats are available for download in API.",
                "num_resources": 4,
                "num_tags": 0,
                "organization": {
                    "id": "89fab59e-35c9-45c6-bad2-f17be25bd86d",
                    "name": "hk-hyd",
                    "title": "Highways Department",
                    "type": "organization",
                    "description": "",
                    "image_url": "https://data.gov.hk/filestore/provider-images/hk-hyd.png",
                    "created": "2021-07-02T10:54:54.878679",
                    "is_organization": True,
                    "approval_status": "approved",
                    "state": "active"
                },
                "owner_org": "89fab59e-35c9-45c6-bad2-f17be25bd86d",
                "private": False,
                "state": "active",
                "title": "Lamp Post Location Data",
                "type": "dataset",
                "update_frequency": "Quarterly",
                "url": None,
                "version": None,
                "groups": [{
                    "description": "",
                    "display_name": "City Management and Utilities",
                    "id": "ec24df17-6be5-4283-b9b9-f4a9100bb618",
                    "image_display_url": "",
                    "name": "city-management",
                    "title": "City Management and Utilities"
                }],
                "resources": [
                    {
                        "cache_last_updated": None,
                        "cache_url": None,
                        "created": "2025-06-24T16:32:01.791534",
                        "dateCreated": "2026-06-24",
                        "dateModified": "2026-06-24",
                        "datePublished": "2019-06-26",
                        "description": "Lamp Post Location Data (English)",
                        "format": "CSV",
                        "hash": "",
                        "id": "1c7f0826-6f41-4804-8725-cfa2284f46db",
                        "inLanguage": "en",
                        "is_api": "N",
                        "last_modified": None,
                        "metadata_modified": "2025-06-24T16:32:01.785357",
                        "mimetype": None,
                        "mimetype_inner": None,
                        "name": "Lamp Post Location Data (English)",
                        "package_id": "770755cb-2a71-4d85-bff3-6b183dea3129",
                        "position": 0,
                        "resource_type": None,
                        "schema": "https://plis.hyd.gov.hk/datagovhk/plis/PLIS-PSI-data-schema_EN.txt",
                        "shared_id": "c195e044511811f09b050a58c0a84b88",
                        "size": None,
                        "state": "active",
                        "temporal_from": "24/06/2026",
                        "temporal_to": "24/06/2026",
                        "url": "https://plis.hyd.gov.hk/datagovhk/plis/lamppost_en.csv",
                        "url_type": None
                    },
                    {
                        "cache_last_updated": None,
                        "cache_url": None,
                        "created": "2025-06-24T16:32:02.578053",
                        "dateCreated": "2026-06-24",
                        "dateModified": "2026-06-24",
                        "datePublished": "2019-06-26",
                        "description": "Lamp Post Location Data (Traditional Chinese)",
                        "format": "CSV",
                        "hash": "",
                        "id": "bc141870-799c-437d-a86b-5345cb2b3f1c",
                        "inLanguage": "zh-Hant",
                        "is_api": "N",
                        "last_modified": None,
                        "metadata_modified": "2025-06-24T16:32:02.572103",
                        "mimetype": None,
                        "mimetype_inner": None,
                        "name": "Lamp Post Location Data (Traditional Chinese)",
                        "package_id": "770755cb-2a71-4d85-bff3-6b183dea3129",
                        "position": 1,
                        "resource_type": None,
                        "schema": "https://plis.hyd.gov.hk/datagovhk/plis/PLIS-PSI-data-schema_TC.txt",
                        "shared_id": "c20e5074511811f09b050a58c0a84b88",
                        "size": None,
                        "state": "active",
                        "temporal_from": "24/06/2026",
                        "temporal_to": "24/06/2026",
                        "url": "https://plis.hyd.gov.hk/datagovhk/plis/lamppost_tc.csv",
                        "url_type": None
                    }
                ],
                "tags": [],
                "relationships_as_subject": [],
                "relationships_as_object": []
            }
        }

    @patch('requests.get')
    def test_get_package_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_package_data(id="hk-hyd-plis-lamppostdata", language="en")
        self.assertEqual(result, self.sample_data)
        mock_get.assert_called_once_with(
            "https://data.gov.hk/en-data/api/3/action/package_show?id=hk-hyd-plis-lamppostdata",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )

    @patch('requests.get')
    def test_get_package_data_different_language(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_package_data(id="hk-hyd-plis-lamppostdata", language="tc")
        self.assertEqual(result, self.sample_data)
        mock_get.assert_called_once_with(
            "https://data.gov.hk/tc-data/api/3/action/package_show?id=hk-hyd-plis-lamppostdata",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )

    @patch('requests.get')
    def test_get_package_data_invalid_language(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.sample_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_package_data(id="hk-hyd-plis-lamppostdata", language="invalid")
        self.assertEqual(result, self.sample_data)
        mock_get.assert_called_once_with(
            "https://data.gov.hk/en-data/api/3/action/package_show?id=hk-hyd-plis-lamppostdata",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )

    @patch('requests.get')
    def test_get_package_data_request_exception(self, mock_get):
        mock_get.side_effect = Exception("Request failed")

        result = get_package_data(id="hk-hyd-plis-lamppostdata", language="en")
        self.assertIn("error", result)
        self.assertIn("Request failed", result["error"])

    @patch('requests.get')
    def test_get_package_data_empty_id(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"error": "Invalid ID"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_package_data(id="")
        self.assertIn("error", result)
        mock_get.assert_called_once_with(
            "https://data.gov.hk/en-data/api/3/action/package_show?id=",
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
            }
        )

if __name__ == '__main__':
    unittest.main()
