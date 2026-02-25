"""CLI orchestrator for the IRS 990 ingestion pipeline."""

import argparse
import logging

from sqlalchemy.orm import Session

from scripts.ingest.config import HISTORICAL_YEARS
from scripts.ingest.downloader import download_xml
from scripts.ingest.index_downloader import download_index
from scripts.ingest.loader import get_session_factory, load_filing
from scripts.ingest.xml_parser import parse_filing

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def run_pipeline(mode: str, limit: int | None = None):
    """Run the ingestion pipeline."""
    if mode == "historical":
        years = HISTORICAL_YEARS
        effective_limit = limit if limit is not None else 100_000
    else:
        # Incremental: latest year only
        years = [HISTORICAL_YEARS[-1]]
        effective_limit = limit  # None means no limit

    logger.info("Starting %s ingestion for years: %s", mode, years)

    session_factory = get_session_factory()
    total = 0
    success = 0
    skipped = 0
    errors = 0

    for year in years:
        entries = download_index(year)
        if not entries:
            logger.warning("No entries for year %d", year)
            continue

        for entry in entries:
            if effective_limit is not None and total >= effective_limit:
                logger.info("Reached limit of %d filings", effective_limit)
                break

            total += 1

            try:
                xml_bytes = download_xml(entry.object_id)
                if xml_bytes is None:
                    errors += 1
                    continue

                parsed = parse_filing(xml_bytes)
                if parsed is None:
                    errors += 1
                    continue

                with Session(session_factory.kw["bind"]) as session:
                    loaded = load_filing(session, parsed, entry.object_id)
                    session.commit()

                if loaded:
                    success += 1
                else:
                    skipped += 1

            except Exception:
                errors += 1
                logger.exception("Error processing filing %s", entry.object_id)

            if total % 100 == 0:
                logger.info(
                    "Processed %d filings (%d success, %d skipped, %d errors)",
                    total,
                    success,
                    skipped,
                    errors,
                )

        else:
            continue
        break  # Break outer loop if inner loop hit limit

    logger.info(
        "Done. Processed %d filings, %d loaded, %d skipped, %d errors",
        total,
        success,
        skipped,
        errors,
    )


def main():
    parser = argparse.ArgumentParser(description="IRS 990 Data Ingestion Pipeline")
    parser.add_argument(
        "--mode",
        choices=["historical", "incremental"],
        default="historical",
        help="Ingestion mode (default: historical)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max number of filings to process",
    )
    args = parser.parse_args()
    run_pipeline(mode=args.mode, limit=args.limit)


if __name__ == "__main__":
    main()
