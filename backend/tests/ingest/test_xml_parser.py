"""Tests for the XML parser."""

from pathlib import Path

from scripts.ingest.xml_parser import parse_filing

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _read_fixture(filename: str) -> bytes:
    return (FIXTURES_DIR / filename).read_bytes()


# --- 990 Tests ---


class TestForm990_2014Plus:
    def setup_method(self):
        self.result = parse_filing(_read_fixture("form_990_2014plus.xml"))

    def test_parsed_not_none(self):
        assert self.result is not None

    def test_header_fields(self):
        assert self.result.ein == "123456789"
        assert self.result.name == "Test Organization 990"
        assert self.result.city == "New York"
        assert self.result.state == "NY"
        assert self.result.tax_year == 2022
        assert self.result.form_type == "990"

    def test_financial_fields(self):
        assert self.result.total_revenue == 5_000_000
        assert self.result.total_expenses == 4_500_000
        assert self.result.net_assets == 2_000_000
        assert self.result.contributions_and_grants == 3_000_000
        assert self.result.program_service_revenue == 1_500_000
        assert self.result.investment_income == 500_000
        assert self.result.program_expenses == 3_500_000
        assert self.result.management_expenses == 700_000
        assert self.result.fundraising_expenses == 300_000
        assert self.result.num_employees == 150
        assert self.result.num_volunteers == 500

    def test_mission(self):
        assert self.result.mission_description == (
            "Helping communities thrive through education and outreach."
        )

    def test_people_extracted(self):
        assert len(self.result.people) == 2
        director = self.result.people[0]
        assert director.name == "Jane Smith"
        assert director.title == "Executive Director"
        assert director.compensation == 250_000
        assert director.is_officer is True
        assert director.is_director is False

        board = self.result.people[1]
        assert board.name == "John Doe"
        assert board.title == "Board Chair"
        assert board.is_director is True
        assert board.is_officer is False

    def test_no_grants(self):
        assert self.result.grants == []


class TestForm990_Pre2014:
    def setup_method(self):
        self.result = parse_filing(_read_fixture("form_990_pre2014.xml"))

    def test_parsed_not_none(self):
        assert self.result is not None

    def test_header_fields(self):
        assert self.result.ein == "987654321"
        assert self.result.name == "Pre-2014 Test Org"
        assert self.result.city == "Chicago"
        assert self.result.state == "IL"
        assert self.result.tax_year == 2012
        assert self.result.form_type == "990"

    def test_fallback_financial_fields(self):
        assert self.result.total_revenue == 3_000_000
        assert self.result.total_expenses == 2_800_000
        assert self.result.net_assets == 1_500_000
        assert self.result.contributions_and_grants == 2_000_000
        assert self.result.program_service_revenue == 800_000
        assert self.result.investment_income == 200_000
        assert self.result.program_expenses == 2_200_000
        assert self.result.management_expenses == 400_000
        assert self.result.fundraising_expenses == 200_000
        assert self.result.num_employees == 75
        assert self.result.num_volunteers == 200

    def test_mission(self):
        assert "health research" in self.result.mission_description

    def test_people_extracted(self):
        assert len(self.result.people) == 1
        person = self.result.people[0]
        assert person.name == "Alice Johnson"
        assert person.title == "CEO"
        assert person.compensation == 180_000
        assert person.is_officer is True


class TestForm990_MissingFields:
    def setup_method(self):
        self.result = parse_filing(_read_fixture("form_990_missing_fields.xml"))

    def test_parsed_not_none(self):
        assert self.result is not None

    def test_header_fields(self):
        assert self.result.ein == "111222333"
        assert self.result.name == "Minimal Org"

    def test_present_field(self):
        assert self.result.total_revenue == 1_000_000

    def test_missing_fields_are_none(self):
        assert self.result.total_expenses is None
        assert self.result.net_assets is None
        assert self.result.contributions_and_grants is None
        assert self.result.program_service_revenue is None
        assert self.result.investment_income is None
        assert self.result.program_expenses is None
        assert self.result.management_expenses is None
        assert self.result.fundraising_expenses is None
        assert self.result.num_employees is None
        assert self.result.num_volunteers is None
        assert self.result.mission_description is None

    def test_no_people(self):
        assert self.result.people == []


# --- 990-EZ Tests ---


class TestForm990EZ_2014Plus:
    def setup_method(self):
        self.result = parse_filing(_read_fixture("form_990ez_2014plus.xml"))

    def test_parsed_not_none(self):
        assert self.result is not None

    def test_header_fields(self):
        assert self.result.ein == "444555666"
        assert self.result.name == "Small Charity EZ"
        assert self.result.city == "Austin"
        assert self.result.state == "TX"
        assert self.result.tax_year == 2022
        assert self.result.form_type == "990EZ"

    def test_financial_fields(self):
        assert self.result.total_revenue == 150_000
        assert self.result.total_expenses == 140_000
        assert self.result.net_assets == 50_000
        assert self.result.contributions_and_grants == 120_000
        assert self.result.program_service_revenue == 20_000
        assert self.result.investment_income == 10_000

    def test_no_990_specific_fields(self):
        # 990EZ doesn't have these fields in the field map
        assert self.result.program_expenses is None
        assert self.result.management_expenses is None
        assert self.result.fundraising_expenses is None

    def test_no_people_or_grants(self):
        assert self.result.people == []
        assert self.result.grants == []


class TestForm990EZ_Pre2014:
    def setup_method(self):
        self.result = parse_filing(_read_fixture("form_990ez_pre2014.xml"))

    def test_parsed_not_none(self):
        assert self.result is not None

    def test_header_fields(self):
        assert self.result.ein == "555666777"
        assert self.result.name == "Old Small Charity"
        assert self.result.city == "Denver"
        assert self.result.state == "CO"
        assert self.result.tax_year == 2012
        assert self.result.form_type == "990EZ"

    def test_fallback_financial_fields(self):
        assert self.result.total_revenue == 100_000
        assert self.result.total_expenses == 95_000
        assert self.result.net_assets == 30_000
        assert self.result.contributions_and_grants == 80_000
        assert self.result.program_service_revenue == 15_000
        assert self.result.investment_income == 5_000


class TestForm990EZ_MissingFields:
    def setup_method(self):
        self.result = parse_filing(_read_fixture("form_990ez_missing_fields.xml"))

    def test_parsed_not_none(self):
        assert self.result is not None

    def test_present_field(self):
        assert self.result.total_revenue == 50_000

    def test_missing_fields_are_none(self):
        assert self.result.total_expenses is None
        assert self.result.net_assets is None


# --- 990-PF Tests ---


class TestForm990PF_2014Plus:
    def setup_method(self):
        self.result = parse_filing(_read_fixture("form_990pf_2014plus.xml"))

    def test_parsed_not_none(self):
        assert self.result is not None

    def test_header_fields(self):
        assert self.result.ein == "777888999"
        assert self.result.name == "Test Foundation PF"
        assert self.result.city == "San Francisco"
        assert self.result.state == "CA"
        assert self.result.tax_year == 2022
        assert self.result.form_type == "990PF"

    def test_financial_fields(self):
        assert self.result.total_revenue == 10_000_000
        assert self.result.total_expenses == 8_000_000
        assert self.result.net_assets == 50_000_000
        assert self.result.contributions_and_grants == 500_000
        assert self.result.investment_income == 9_500_000

    def test_grants_extracted(self):
        assert len(self.result.grants) == 2
        grant1 = self.result.grants[0]
        assert grant1.recipient_name == "Local School District"
        assert grant1.recipient_city == "San Francisco"
        assert grant1.recipient_state == "CA"
        assert grant1.amount == 250_000
        assert grant1.purpose == "Support STEM education programs"

        grant2 = self.result.grants[1]
        assert grant2.recipient_name == "Community Health Center"
        assert grant2.amount == 100_000

    def test_no_people(self):
        assert self.result.people == []


class TestForm990PF_Pre2014:
    def setup_method(self):
        self.result = parse_filing(_read_fixture("form_990pf_pre2014.xml"))

    def test_parsed_not_none(self):
        assert self.result is not None

    def test_header_fields(self):
        assert self.result.ein == "888999000"
        assert self.result.name == "Old Foundation PF"
        assert self.result.city == "Seattle"
        assert self.result.state == "WA"
        assert self.result.tax_year == 2012
        assert self.result.form_type == "990PF"

    def test_fallback_financial_fields(self):
        assert self.result.total_revenue == 7_000_000
        assert self.result.total_expenses == 5_000_000
        assert self.result.net_assets == 40_000_000
        assert self.result.contributions_and_grants == 300_000
        assert self.result.investment_income == 6_700_000

    def test_grants_extracted(self):
        assert len(self.result.grants) == 1
        grant = self.result.grants[0]
        assert grant.recipient_name == "Youth Arts Program"
        assert grant.recipient_city == "Seattle"
        assert grant.recipient_state == "WA"
        assert grant.amount == 75_000
        assert grant.purpose == "Arts education for underserved youth"


class TestForm990PF_MissingFields:
    def setup_method(self):
        self.result = parse_filing(_read_fixture("form_990pf_missing_fields.xml"))

    def test_parsed_not_none(self):
        assert self.result is not None

    def test_present_field(self):
        assert self.result.total_revenue == 2_000_000

    def test_missing_fields_are_none(self):
        assert self.result.total_expenses is None
        assert self.result.net_assets is None

    def test_no_grants(self):
        assert self.result.grants == []


# --- Edge Cases ---


class TestEdgeCases:
    def test_malformed_xml_returns_none(self):
        result = parse_filing(b"<not valid xml!!!")
        assert result is None

    def test_empty_bytes_returns_none(self):
        result = parse_filing(b"")
        assert result is None

    def test_xml_without_ein_returns_none(self):
        xml = b"""<?xml version="1.0" encoding="utf-8"?>
        <Return xmlns="http://www.irs.gov/efile" returnVersion="2022v5.0">
          <ReturnHeader>
            <ReturnTypeCd>990</ReturnTypeCd>
            <TaxYr>2022</TaxYr>
            <Filer>
              <BusinessName>
                <BusinessNameLine1Txt>No EIN Org</BusinessNameLine1Txt>
              </BusinessName>
            </Filer>
          </ReturnHeader>
          <ReturnData><IRS990></IRS990></ReturnData>
        </Return>"""
        result = parse_filing(xml)
        assert result is None
