import uuid
from datetime import date

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, FullTimestampMixin, TimestampMixin, UUIDMixin


class Organization(Base, UUIDMixin, FullTimestampMixin):
    __tablename__ = "organizations"

    ein: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str | None] = mapped_column(Text)
    state: Mapped[str | None] = mapped_column(String(2))
    ntee_code: Mapped[str | None] = mapped_column(String(10))
    ruling_date: Mapped[date | None] = mapped_column(Date)

    filings: Mapped[list["Filing"]] = relationship(back_populates="organization")

    __table_args__ = (
        Index("idx_org_ein", "ein"),
        Index("idx_org_state", "state"),
        Index("idx_org_ntee", "ntee_code"),
        Index(
            "idx_org_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )


class Filing(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "filings"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id"), nullable=False
    )
    object_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    tax_year: Mapped[int] = mapped_column(Integer, nullable=False)
    filing_type: Mapped[str] = mapped_column(String(10), nullable=False)
    filing_date: Mapped[date | None] = mapped_column(Date)
    total_revenue: Mapped[int | None] = mapped_column(BigInteger)
    total_expenses: Mapped[int | None] = mapped_column(BigInteger)
    net_assets: Mapped[int | None] = mapped_column(BigInteger)
    contributions_and_grants: Mapped[int | None] = mapped_column(BigInteger)
    program_service_revenue: Mapped[int | None] = mapped_column(BigInteger)
    investment_income: Mapped[int | None] = mapped_column(BigInteger)
    program_expenses: Mapped[int | None] = mapped_column(BigInteger)
    management_expenses: Mapped[int | None] = mapped_column(BigInteger)
    fundraising_expenses: Mapped[int | None] = mapped_column(BigInteger)
    num_employees: Mapped[int | None] = mapped_column(Integer)
    num_volunteers: Mapped[int | None] = mapped_column(Integer)
    mission_description: Mapped[str | None] = mapped_column(Text)
    raw_xml_url: Mapped[str | None] = mapped_column(Text)

    organization: Mapped["Organization"] = relationship(back_populates="filings")
    people: Mapped[list["FilingPerson"]] = relationship(back_populates="filing")
    grants: Mapped[list["FilingGrant"]] = relationship(back_populates="filing")

    __table_args__ = (
        Index("idx_filing_org", "organization_id"),
        Index("idx_filing_year", "tax_year"),
        Index("idx_filing_type", "filing_type"),
    )


class FilingPerson(Base, UUIDMixin):
    __tablename__ = "filing_people"

    filing_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("filings.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str | None] = mapped_column(Text)
    compensation: Mapped[int | None] = mapped_column(BigInteger)
    is_officer: Mapped[bool] = mapped_column(Boolean, default=False)
    is_director: Mapped[bool] = mapped_column(Boolean, default=False)
    is_key_employee: Mapped[bool] = mapped_column(Boolean, default=False)
    is_highest_compensated: Mapped[bool] = mapped_column(Boolean, default=False)

    filing: Mapped["Filing"] = relationship(back_populates="people")

    __table_args__ = (Index("idx_people_filing", "filing_id"),)


class FilingGrant(Base, UUIDMixin):
    __tablename__ = "filing_grants"

    filing_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("filings.id"), nullable=False
    )
    recipient_name: Mapped[str] = mapped_column(Text, nullable=False)
    recipient_ein: Mapped[str | None] = mapped_column(String(10))
    recipient_city: Mapped[str | None] = mapped_column(Text)
    recipient_state: Mapped[str | None] = mapped_column(String(2))
    amount: Mapped[int | None] = mapped_column(BigInteger)
    purpose: Mapped[str | None] = mapped_column(Text)

    filing: Mapped["Filing"] = relationship(back_populates="grants")

    __table_args__ = (Index("idx_grants_filing", "filing_id"),)
