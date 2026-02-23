import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class UsageEvent(Base, UUIDMixin):
    __tablename__ = "usage_events"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (Index("idx_usage_user_date", "user_id", "created_at"),)


class OrgSummary(Base, UUIDMixin):
    __tablename__ = "org_summaries"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id"), nullable=False
    )
    filing_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("filings.id"))
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    model_version: Mapped[str | None] = mapped_column(String(50))
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class OrgScore(Base, UUIDMixin):
    __tablename__ = "org_scores"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id"), nullable=False
    )
    filing_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("filings.id"), nullable=False
    )
    overall_score: Mapped[int] = mapped_column(Integer, nullable=False)
    revenue_diversity_score: Mapped[int | None] = mapped_column(Integer)
    operating_reserves_score: Mapped[int | None] = mapped_column(Integer)
    fundraising_efficiency_score: Mapped[int | None] = mapped_column(Integer)
    program_expense_ratio_score: Mapped[int | None] = mapped_column(Integer)
    revenue_growth_score: Mapped[int | None] = mapped_column(Integer)
    working_capital_score: Mapped[int | None] = mapped_column(Integer)
    peer_percentile: Mapped[int | None] = mapped_column(Integer)
    scored_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
