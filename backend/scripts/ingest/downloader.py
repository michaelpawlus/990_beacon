"""Downloads ZIP archives of XML files from the IRS TEOS endpoint.

Memory-safe: streams ZIPs to disk and yields one XML at a time.
"""

import gc
import logging
import os
import tempfile
import time
import zipfile
from collections.abc import Generator
from contextlib import contextmanager

import requests

from scripts.ingest.config import (
    IRS_ZIP_TEMPLATE,
    MAX_RETRIES,
    MAX_ZIP_SIZE_BYTES,
    MAX_ZIP_SIZE_MB,
    RETRY_BACKOFF_BASE,
    STREAM_CHUNK_SIZE,
)

logger = logging.getLogger(__name__)


def _check_content_length(url: str) -> int | None:
    """HEAD request to get Content-Length. Returns bytes or None."""
    try:
        resp = requests.head(url, timeout=30, allow_redirects=True)
        resp.raise_for_status()
        cl = resp.headers.get("Content-Length")
        return int(cl) if cl else None
    except (requests.RequestException, ValueError):
        return None


def _download_to_tempfile(url: str) -> str | None:
    """Stream a ZIP to a temp file on disk. Returns path or None."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, timeout=300, stream=True)
            resp.raise_for_status()

            fd, tmp_path = tempfile.mkstemp(suffix=".zip")
            try:
                total = 0
                with os.fdopen(fd, "wb") as f:
                    for chunk in resp.iter_content(
                        chunk_size=STREAM_CHUNK_SIZE
                    ):
                        f.write(chunk)
                        total += len(chunk)
            except Exception:
                os.unlink(tmp_path)
                raise

            size_mb = total / (1024 * 1024)
            logger.info(
                "Downloaded %s to disk: %.1f MB", url.split("/")[-1], size_mb
            )
            return tmp_path

        except requests.RequestException as exc:
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF_BASE**attempt
                logger.warning(
                    "Attempt %d/%d failed for %s: %s. Retrying in %ds...",
                    attempt,
                    MAX_RETRIES,
                    url,
                    exc,
                    wait,
                )
                time.sleep(wait)
            else:
                logger.warning(
                    "All %d attempts failed for %s: %s",
                    MAX_RETRIES,
                    url,
                    exc,
                )

    return None


@contextmanager
def open_zip_batch(
    year: int, batch_id: str
) -> Generator[Generator[tuple[str, bytes], None, None] | None, None, None]:
    """Context manager that downloads a ZIP to disk and yields XML entries.

    Yields a generator of (filename, xml_bytes) tuples one at a time,
    or None if the download fails or the ZIP is too large.

    Usage::

        with open_zip_batch(2024, "batch01") as xml_iter:
            if xml_iter is None:
                continue
            for filename, xml_bytes in xml_iter:
                process(xml_bytes)
    """
    url = IRS_ZIP_TEMPLATE.format(year=year, batch_id=batch_id)

    # Check size before downloading
    content_length = _check_content_length(url)
    if content_length is not None and content_length > MAX_ZIP_SIZE_BYTES:
        size_mb = content_length / (1024 * 1024)
        logger.warning(
            "Skipping %s: %.0f MB exceeds %d MB limit",
            batch_id,
            size_mb,
            MAX_ZIP_SIZE_MB,
        )
        yield None
        return

    tmp_path = _download_to_tempfile(url)
    if tmp_path is None:
        yield None
        return

    try:

        def _xml_entries() -> Generator[tuple[str, bytes], None, None]:
            try:
                with zipfile.ZipFile(tmp_path, "r") as zf:
                    for name in zf.namelist():
                        if name.lower().endswith(".xml"):
                            yield name, zf.read(name)
            except zipfile.BadZipFile as exc:
                logger.warning("Bad ZIP file for %s: %s", batch_id, exc)

        yield _xml_entries()
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        gc.collect()
