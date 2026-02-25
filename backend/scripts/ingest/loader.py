"""Loads parsed filing data into PostgreSQL using sync SQLAlchemy."""

import logging
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.models.organization import Filing, FilingGrant, FilingPerson, Organization
from scripts.ingest.xml_parser import ParsedFiling

logger = logging.getLogger(__name__)

DEFAULT_DB_URL = "postgresql+psycopg://beacon:beacon@localhost:5432/beacon_dev"


def get_engine(db_url: str | None = None):
    url = db_url or os.environ.get("DATABASE_URL_SYNC", DEFAULT_DB_URL)
    return create_engine(url)


def get_session_factory(db_url: str | None = None):
    engine = get_engine(db_url)
    return sessionmaker(bind=engine)


def load_filing(session: Session, parsed: ParsedFiling, object_id: str) -> bool:
    """Load a parsed filing into the database.

    Returns True if the filing was inserted, False if it was skipped
    (already exists with the same object_id).
    """
    # Idempotency: skip if filing with this object_id already exists
    existing = session.execute(
        select(Filing).where(Filing.object_id == object_id)
    ).scalar_one_or_none()

    if existing is not None:
        logger.debug("Filing %s already exists, skipping", object_id)
        return False

    # Upsert organization by EIN
    org = session.execute(
        select(Organization).where(Organization.ein == parsed.ein)
    ).scalar_one_or_none()

    if org is None:
        org = Organization(
            ein=parsed.ein,
            name=parsed.name,
            city=parsed.city,
            state=parsed.state,
        )
        session.add(org)
        session.flush()
        logger.debug("Created organization: %s (%s)", parsed.name, parsed.ein)
    else:
        # Update org info with latest filing data
        org.name = parsed.name
        if parsed.city:
            org.city = parsed.city
        if parsed.state:
            org.state = parsed.state
        session.flush()

    # Insert filing
    filing = Filing(
        organization_id=org.id,
        object_id=object_id,
        tax_year=parsed.tax_year or 0,
        filing_type=parsed.form_type or "990",
        total_revenue=parsed.total_revenue,
        total_expenses=parsed.total_expenses,
        net_assets=parsed.net_assets,
        contributions_and_grants=parsed.contributions_and_grants,
        program_service_revenue=parsed.program_service_revenue,
        investment_income=parsed.investment_income,
        program_expenses=parsed.program_expenses,
        management_expenses=parsed.management_expenses,
        fundraising_expenses=parsed.fundraising_expenses,
        num_employees=parsed.num_employees,
        num_volunteers=parsed.num_volunteers,
        mission_description=parsed.mission_description,
        raw_xml_url=None,
    )
    session.add(filing)
    session.flush()

    # Insert people
    for person in parsed.people:
        fp = FilingPerson(
            filing_id=filing.id,
            name=person.name,
            title=person.title,
            compensation=person.compensation,
            is_officer=person.is_officer,
            is_director=person.is_director,
            is_key_employee=person.is_key_employee,
            is_highest_compensated=person.is_highest_compensated,
        )
        session.add(fp)

    # Insert grants
    for grant in parsed.grants:
        fg = FilingGrant(
            filing_id=filing.id,
            recipient_name=grant.recipient_name,
            recipient_ein=grant.recipient_ein,
            recipient_city=grant.recipient_city,
            recipient_state=grant.recipient_state,
            amount=grant.amount,
            purpose=grant.purpose,
        )
        session.add(fg)

    session.flush()
    return True
