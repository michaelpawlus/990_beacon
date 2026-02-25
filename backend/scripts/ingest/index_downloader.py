"""Downloads and parses IRS index CSV files."""

import csv
import io
import logging
from dataclasses import dataclass

import requests

from scripts.ingest.config import IRS_INDEX_CSV_TEMPLATE, VALID_FILING_TYPES

logger = logging.getLogger(__name__)


@dataclass
class IndexEntry:
    object_id: str
    ein: str
    taxpayer_name: str
    return_type: str
    tax_period: str
    sub_date: str
    xml_batch_id: str


def download_index(year: int) -> list[IndexEntry]:
    """Download and parse the IRS index CSV for a given year.

    Returns a list of IndexEntry for valid 990/990EZ/990PF filings.
    """
    url = IRS_INDEX_CSV_TEMPLATE.format(year=year)
    logger.info("Downloading index for year %d from %s", year, url)

    try:
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
    except Exception as exc:
        logger.warning("Failed to download index for year %d: %s", year, exc)
        return []

    entries: list[IndexEntry] = []
    reader = csv.DictReader(io.StringIO(resp.text))

    for row in reader:
        return_type = row.get("RETURN_TYPE", "")
        if return_type not in VALID_FILING_TYPES:
            continue

        entries.append(
            IndexEntry(
                object_id=row.get("OBJECT_ID", ""),
                ein=row.get("EIN", ""),
                taxpayer_name=row.get("TAXPAYER_NAME", ""),
                return_type=return_type,
                tax_period=row.get("TAX_PERIOD", ""),
                sub_date=row.get("SUB_DATE", ""),
                xml_batch_id=row.get("XML_BATCH_ID", ""),
            )
        )

    logger.info("Parsed %d valid entries for year %d", len(entries), year)
    return entries
