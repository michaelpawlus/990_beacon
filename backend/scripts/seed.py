"""Seed script for local development. Creates sample data. Idempotent."""

import os
import sys

# Add backend root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Filing, Organization, User, Watchlist, WatchlistItem


def get_sync_url() -> str:
    url = settings.DATABASE_URL
    if "+asyncpg" in url:
        url = url.replace("+asyncpg", "+psycopg")
    return url


SAMPLE_ORGS = [
    {
        "ein": "131624100",
        "name": "United Way Worldwide",
        "city": "Alexandria",
        "state": "VA",
        "ntee_code": "T20",
    },
    {
        "ein": "530196605",
        "name": "American Red Cross",
        "city": "Washington",
        "state": "DC",
        "ntee_code": "P20",
    },
    {
        "ein": "135562162",
        "name": "Salvation Army",
        "city": "Alexandria",
        "state": "VA",
        "ntee_code": "P20",
    },
    {
        "ein": "362167940",
        "name": "Feeding America",
        "city": "Chicago",
        "state": "IL",
        "ntee_code": "K31",
    },
    {
        "ein": "582492502",
        "name": "Habitat for Humanity International",
        "city": "Americus",
        "state": "GA",
        "ntee_code": "L21",
    },
]


def seed():
    engine = create_engine(get_sync_url())
    with Session(engine) as session:
        # Create test user (idempotent)
        existing_user = session.execute(
            select(User).where(User.clerk_id == "user_seed_test")
        ).scalar_one_or_none()

        if existing_user is None:
            user = User(
                clerk_id="user_seed_test",
                email="dev@990beacon.com",
                full_name="Dev User",
                plan_tier="pro",
            )
            session.add(user)
            session.flush()
            print("Created test user: dev@990beacon.com")
        else:
            user = existing_user
            print("Test user already exists, skipping")

        # Create sample organizations (idempotent)
        org_ids = []
        for org_data in SAMPLE_ORGS:
            existing = session.execute(
                select(Organization).where(Organization.ein == org_data["ein"])
            ).scalar_one_or_none()

            if existing is None:
                org = Organization(**org_data)
                session.add(org)
                session.flush()
                org_ids.append(org.id)
                print(f"Created org: {org_data['name']}")

                # Add a sample filing
                filing = Filing(
                    organization_id=org.id,
                    object_id=f"seed-{org_data['ein']}-2023",
                    tax_year=2023,
                    filing_type="990",
                    total_revenue=50_000_000,
                    total_expenses=48_000_000,
                    net_assets=25_000_000,
                )
                session.add(filing)
            else:
                org_ids.append(existing.id)
                print(f"Org already exists: {org_data['name']}, skipping")

        # Create a watchlist (idempotent)
        existing_wl = session.execute(
            select(Watchlist).where(
                Watchlist.user_id == user.id,
                Watchlist.name == "My Prospects",
            )
        ).scalar_one_or_none()

        if existing_wl is None:
            watchlist = Watchlist(
                user_id=user.id,
                name="My Prospects",
            )
            session.add(watchlist)
            session.flush()

            for oid in org_ids[:3]:
                item = WatchlistItem(
                    watchlist_id=watchlist.id,
                    organization_id=oid,
                )
                session.add(item)
            print("Created watchlist: My Prospects (3 items)")
        else:
            print("Watchlist already exists, skipping")

        session.commit()
        print("\nSeed complete!")


if __name__ == "__main__":
    seed()
