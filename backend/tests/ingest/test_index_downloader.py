"""Tests for the IRS index CSV downloader."""

from unittest.mock import MagicMock, patch

from scripts.ingest.index_downloader import IndexEntry, download_index

SAMPLE_CSV = (
    "RETURN_ID,FILING_TYPE,EIN,TAX_PERIOD,SUB_DATE,"
    "TAXPAYER_NAME,RETURN_TYPE,DLN,OBJECT_ID,XML_BATCH_ID\n"
    "1001,EFILE,123456789,202212,2023-05-15,"
    "Test Org,990,12345,201900001,2023_TEOS_XML_01A\n"
    "1002,EFILE,987654321,202212,2023-06-01,"
    "Another Org,990EZ,12346,201900002,2023_TEOS_XML_01A\n"
    "1003,EFILE,111222333,202212,2023-07-01,"
    "Foundation Inc,990PF,12347,201900003,2023_TEOS_XML_02A\n"
    "1004,EFILE,444555666,202212,2023-08-01,"
    "Bad Type,990T,12348,201900004,2023_TEOS_XML_02A\n"
)


class TestDownloadIndex:
    @patch("scripts.ingest.index_downloader.requests.get")
    def test_parses_valid_entries(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = SAMPLE_CSV
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        entries = download_index(2022)

        assert len(entries) == 3
        assert all(isinstance(e, IndexEntry) for e in entries)

    @patch("scripts.ingest.index_downloader.requests.get")
    def test_filters_invalid_return_types(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = SAMPLE_CSV
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        entries = download_index(2022)

        return_types = {e.return_type for e in entries}
        assert return_types == {"990", "990EZ", "990PF"}

    @patch("scripts.ingest.index_downloader.requests.get")
    def test_entry_fields_populated(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = SAMPLE_CSV
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        entries = download_index(2022)

        entry = entries[0]
        assert entry.object_id == "201900001"
        assert entry.ein == "123456789"
        assert entry.taxpayer_name == "Test Org"
        assert entry.return_type == "990"
        assert entry.tax_period == "202212"
        assert entry.sub_date == "2023-05-15"
        assert entry.xml_batch_id == "2023_TEOS_XML_01A"

    @patch("scripts.ingest.index_downloader.requests.get")
    def test_http_error_returns_empty(self, mock_get):
        mock_get.side_effect = Exception("Connection error")

        entries = download_index(2022)

        assert entries == []

    @patch("scripts.ingest.index_downloader.requests.get")
    def test_http_status_error_returns_empty(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_resp

        entries = download_index(2099)

        assert entries == []

    @patch("scripts.ingest.index_downloader.requests.get")
    def test_uses_correct_url(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = SAMPLE_CSV
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        download_index(2023)

        call_url = mock_get.call_args[0][0]
        assert "index_2023.csv" in call_url
        assert "apps.irs.gov" in call_url
