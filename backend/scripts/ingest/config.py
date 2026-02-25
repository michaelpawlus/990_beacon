"""Ingestion pipeline configuration."""

# IRS TEOS download base URL (moved from S3 in late 2021)
IRS_BASE_URL = "https://apps.irs.gov/pub/epostcard/990/xml"
IRS_INDEX_CSV_TEMPLATE = (
    "https://apps.irs.gov/pub/epostcard/990/xml/{year}/index_{year}.csv"
)
IRS_ZIP_TEMPLATE = (
    "https://apps.irs.gov/pub/epostcard/990/xml/{year}/{batch_id}.zip"
)

# Batch sizes
BATCH_SIZE = 1000
INDEX_BATCH_SIZE = 5000

# Memory-safety constants
MAX_ZIP_SIZE_MB = 200
MAX_ZIP_SIZE_BYTES = MAX_ZIP_SIZE_MB * 1024 * 1024
STREAM_CHUNK_SIZE = 8192

# Retry config
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2  # seconds

# Valid filing types
VALID_FILING_TYPES = {"990", "990EZ", "990PF"}

# Years to ingest for historical mode
# 2024+ indices include XML_BATCH_ID for ZIP-based download
HISTORICAL_YEARS = [2024]
