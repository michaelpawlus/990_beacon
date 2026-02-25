"""Downloads XML files from the IRS S3 bucket."""

import logging
import time

import requests

from scripts.ingest.config import MAX_RETRIES, RETRY_BACKOFF_BASE, XML_URL_TEMPLATE

logger = logging.getLogger(__name__)


def download_xml(object_id: str) -> bytes | None:
    """Download a single XML filing from the IRS S3 bucket.

    Retries up to MAX_RETRIES times with exponential backoff.
    Returns None on failure.
    """
    url = XML_URL_TEMPLATE.format(object_id=object_id)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            return resp.content
        except requests.RequestException as exc:
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF_BASE**attempt
                logger.warning(
                    "Attempt %d/%d failed for %s: %s. Retrying in %ds...",
                    attempt,
                    MAX_RETRIES,
                    object_id,
                    exc,
                    wait,
                )
                time.sleep(wait)
            else:
                logger.warning(
                    "All %d attempts failed for %s: %s",
                    MAX_RETRIES,
                    object_id,
                    exc,
                )

    return None
