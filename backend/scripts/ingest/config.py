"""Ingestion pipeline configuration."""

# IRS S3 bucket base URLs
IRS_INDEX_BASE_URL = "https://s3.amazonaws.com/irs-form-990"
IRS_INDEX_CSV_TEMPLATE = "https://s3.amazonaws.com/irs-form-990/index_{year}.csv"

# XML download URL template
XML_URL_TEMPLATE = "https://s3.amazonaws.com/irs-form-990/{object_id}_public.xml"

# Batch sizes
BATCH_SIZE = 1000
INDEX_BATCH_SIZE = 5000

# Retry config
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2  # seconds

# Valid filing types
VALID_FILING_TYPES = {"990", "990EZ", "990PF"}

# Years to ingest for historical mode
HISTORICAL_YEARS = [2022, 2023, 2024, 2025]
