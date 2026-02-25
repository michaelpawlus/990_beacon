"""CLI orchestrator for the IRS 990 ingestion pipeline."""

import argparse
import gc
import logging
import resource
from collections import defaultdict

from sqlalchemy.orm import Session

from scripts.ingest.config import HISTORICAL_YEARS
from scripts.ingest.downloader import open_zip_batch
from scripts.ingest.index_downloader import download_index
from scripts.ingest.loader import get_session_factory, load_filing
from scripts.ingest.xml_parser import parse_filing

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _log_memory():
    """Log peak RSS memory usage via stdlib resource module."""
    usage = resource.getrusage(resource.RUSAGE_SELF)
    peak_mb = usage.ru_maxrss / 1024  # Linux reports in KB
    logger.info("Peak RSS memory: %.1f MB", peak_mb)


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
    hit_limit = False

    for year in years:
        if hit_limit:
            break

        entries = download_index(year)
        if not entries:
            logger.warning("No entries for year %d", year)
            continue

        # Group entries by ZIP batch, skip entries without batch_id
        batches: dict[str, list] = defaultdict(list)
        skipped_no_batch = 0
        for entry in entries:
            if not entry.xml_batch_id:
                skipped_no_batch += 1
                continue
            batches[entry.xml_batch_id].append(entry)

        if skipped_no_batch:
            logger.warning(
                "Year %d: skipped %d entries without XML_BATCH_ID",
                year,
                skipped_no_batch,
            )

        logger.info(
            "Year %d: %d entries in %d ZIP batches",
            year,
            len(entries) - skipped_no_batch,
            len(batches),
        )

        for batch_id, batch_entries in batches.items():
            if hit_limit:
                break

            # Build lookup from object_id filename to entry
            entry_lookup = {}
            for e in batch_entries:
                filename = f"{e.object_id}_public.xml"
                entry_lookup[filename] = e

            # Download the ZIP to disk and iterate XMLs
            with open_zip_batch(year, batch_id) as xml_iter:
                if xml_iter is None:
                    logger.warning(
                        "Skipping batch %s (%d entries): "
                        "ZIP download failed or too large",
                        batch_id,
                        len(batch_entries),
                    )
                    continue

                for filename, xml_bytes in xml_iter:
                    if (
                        effective_limit is not None
                        and total >= effective_limit
                    ):
                        logger.info(
                            "Reached limit of %d filings",
                            effective_limit,
                        )
                        hit_limit = True
                        break

                    entry = entry_lookup.get(filename)
                    if entry is None:
                        # XML in ZIP but not in our filtered
                        # index
                        del xml_bytes
                        continue

                    total += 1

                    try:
                        parsed = parse_filing(xml_bytes)
                        del xml_bytes
                        if parsed is None:
                            errors += 1
                            continue

                        with Session(
                            session_factory.kw["bind"]
                        ) as session:
                            loaded = load_filing(
                                session, parsed, entry.object_id
                            )
                            session.commit()

                        if loaded:
                            success += 1
                        else:
                            skipped += 1

                    except Exception:
                        errors += 1
                        logger.exception(
                            "Error processing filing %s",
                            entry.object_id,
                        )

                    if total % 50 == 0:
                        _log_memory()

                    if total % 100 == 0:
                        logger.info(
                            "Processed %d filings "
                            "(%d success, %d skipped, "
                            "%d errors)",
                            total,
                            success,
                            skipped,
                            errors,
                        )

            gc.collect()
            _log_memory()

    logger.info(
        "Done. Processed %d filings, "
        "%d loaded, %d skipped, %d errors",
        total,
        success,
        skipped,
        errors,
    )


def main():
    parser = argparse.ArgumentParser(
        description="IRS 990 Data Ingestion Pipeline"
    )
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
