import pytest

from app.services.profile import compute_metrics


class MockFiling:
    def __init__(self, **kwargs):
        self.tax_year = kwargs.get("tax_year", 2023)
        self.total_revenue = kwargs.get("total_revenue")
        self.total_expenses = kwargs.get("total_expenses")
        self.program_expenses = kwargs.get("program_expenses")
        self.fundraising_expenses = kwargs.get("fundraising_expenses")


class TestComputeMetrics:
    def test_empty_filings(self):
        result = compute_metrics([])
        assert result.program_expense_ratio is None
        assert result.fundraising_efficiency is None
        assert result.revenue_growth_rate is None

    def test_single_filing(self):
        filings = [
            MockFiling(
                total_expenses=1000000,
                program_expenses=800000,
                fundraising_expenses=50000,
                total_revenue=1200000,
            )
        ]
        result = compute_metrics(filings)
        assert result.program_expense_ratio == pytest.approx(0.8)
        assert result.fundraising_efficiency == pytest.approx(0.05)
        assert result.revenue_growth_rate is None  # Need 2 filings

    def test_revenue_growth_positive(self):
        filings = [
            MockFiling(
                tax_year=2023,
                total_revenue=1200000,
                total_expenses=1000000,
                program_expenses=800000,
                fundraising_expenses=50000,
            ),
            MockFiling(
                tax_year=2022,
                total_revenue=1000000,
                total_expenses=900000,
            ),
        ]
        result = compute_metrics(filings)
        assert result.revenue_growth_rate == pytest.approx(0.2)

    def test_revenue_growth_negative(self):
        filings = [
            MockFiling(
                tax_year=2023,
                total_revenue=800000,
                total_expenses=900000,
                program_expenses=700000,
                fundraising_expenses=50000,
            ),
            MockFiling(
                tax_year=2022,
                total_revenue=1000000,
                total_expenses=900000,
            ),
        ]
        result = compute_metrics(filings)
        assert result.revenue_growth_rate == pytest.approx(-0.2)

    def test_zero_denominator_expenses(self):
        filings = [
            MockFiling(
                total_expenses=0,
                program_expenses=0,
                fundraising_expenses=0,
                total_revenue=100,
            )
        ]
        result = compute_metrics(filings)
        assert result.program_expense_ratio is None
        assert result.fundraising_efficiency is None

    def test_zero_denominator_revenue_growth(self):
        filings = [
            MockFiling(
                tax_year=2023,
                total_revenue=100000,
                total_expenses=50000,
                program_expenses=40000,
                fundraising_expenses=5000,
            ),
            MockFiling(tax_year=2022, total_revenue=0),
        ]
        result = compute_metrics(filings)
        assert result.revenue_growth_rate is None

    def test_none_values(self):
        filings = [
            MockFiling(
                total_expenses=None,
                program_expenses=None,
                fundraising_expenses=None,
                total_revenue=None,
            )
        ]
        result = compute_metrics(filings)
        assert result.program_expense_ratio is None
        assert result.fundraising_efficiency is None
