"""XML parser for IRS 990 e-file returns."""

import contextlib
import logging
from dataclasses import dataclass, field

import defusedxml
from lxml import etree
from lxml.etree import XMLSyntaxError

defusedxml.defuse_stdlib()


def _safe_fromstring(xml_bytes: bytes):
    """Parse XML bytes safely, disabling entity expansion."""
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    return etree.fromstring(xml_bytes, parser=parser)

logger = logging.getLogger(__name__)


# --- XPath field maps ---

HEADER_XPATHS = {
    "ein": [
        "//Return/ReturnHeader/Filer/EIN",
        "//Return/ReturnHeader/Filer/EINNumber",
    ],
    "name": [
        "//Return/ReturnHeader/Filer/BusinessName/BusinessNameLine1Txt",
        "//Return/ReturnHeader/Filer/BusinessName/BusinessNameLine1",
        "//Return/ReturnHeader/Filer/Name/BusinessNameLine1",
    ],
    "city": [
        "//Return/ReturnHeader/Filer/USAddress/CityNm",
        "//Return/ReturnHeader/Filer/USAddress/City",
    ],
    "state": [
        "//Return/ReturnHeader/Filer/USAddress/StateAbbreviationCd",
        "//Return/ReturnHeader/Filer/USAddress/State",
    ],
    "tax_year": [
        "//Return/ReturnHeader/TaxYr",
        "//Return/ReturnHeader/TaxYear",
    ],
    "form_type": [
        "//Return/ReturnHeader/ReturnTypeCd",
        "//Return/ReturnHeader/ReturnType",
    ],
}

FIELD_MAPS = {
    "990": {
        "total_revenue": [
            "//Return/ReturnData/IRS990/CYTotalRevenueAmt",
            "//Return/ReturnData/IRS990/TotalRevenueCurrentYear",
            "//Return/ReturnData/IRS990/Revenue/TotalRevenueColumnA",
        ],
        "total_expenses": [
            "//Return/ReturnData/IRS990/CYTotalExpensesAmt",
            "//Return/ReturnData/IRS990/TotalExpensesCurrentYear",
        ],
        "net_assets": [
            "//Return/ReturnData/IRS990/NetAssetsOrFundBalancesEOYAmt",
            "//Return/ReturnData/IRS990/NetAssetsOrFundBalancesBOY",
            "//Return/ReturnData/IRS990/TotalNetAssetsFundBalances/EOY",
        ],
        "contributions_and_grants": [
            "//Return/ReturnData/IRS990/CYContributionsGrantsAmt",
            "//Return/ReturnData/IRS990/ContributionsGrantsCurrentYear",
        ],
        "program_service_revenue": [
            "//Return/ReturnData/IRS990/CYProgramServiceRevenueAmt",
            "//Return/ReturnData/IRS990/ProgramServiceRevenueCY",
        ],
        "investment_income": [
            "//Return/ReturnData/IRS990/CYInvestmentIncomeAmt",
            "//Return/ReturnData/IRS990/InvestmentIncomeCurrentYear",
        ],
        "program_expenses": [
            "//Return/ReturnData/IRS990/CYTotalProgramServiceExpenseAmt",
            "//Return/ReturnData/IRS990/TotalProgramServiceExpense",
        ],
        "management_expenses": [
            "//Return/ReturnData/IRS990/CYManagementAndGeneralAmt",
            "//Return/ReturnData/IRS990/ManagementAndGeneralAmt",
        ],
        "fundraising_expenses": [
            "//Return/ReturnData/IRS990/CYTotalFundraisingExpenseAmt",
            "//Return/ReturnData/IRS990/TotalFundraisingExpense",
            "//Return/ReturnData/IRS990/FundraisingAmt",
        ],
        "num_employees": [
            "//Return/ReturnData/IRS990/TotalEmployeeCnt",
            "//Return/ReturnData/IRS990/TotalNbrEmployees",
        ],
        "num_volunteers": [
            "//Return/ReturnData/IRS990/TotalVolunteersCnt",
            "//Return/ReturnData/IRS990/TotalNbrVolunteers",
        ],
        "mission_description": [
            "//Return/ReturnData/IRS990/ActivityOrMissionDesc",
            "//Return/ReturnData/IRS990/ActivityOrMissionDescription",
            "//Return/ReturnData/IRS990/MissionDescription",
        ],
    },
    "990EZ": {
        "total_revenue": [
            "//Return/ReturnData/IRS990EZ/TotalRevenueAmt",
            "//Return/ReturnData/IRS990EZ/TotalRevenue",
        ],
        "total_expenses": [
            "//Return/ReturnData/IRS990EZ/TotalExpensesAmt",
            "//Return/ReturnData/IRS990EZ/TotalExpenses",
        ],
        "net_assets": [
            "//Return/ReturnData/IRS990EZ/NetAssetsOrFundBalancesEOYAmt",
            "//Return/ReturnData/IRS990EZ/NetAssetsOrFundBalances/EOY",
        ],
        "contributions_and_grants": [
            "//Return/ReturnData/IRS990EZ/ContributionsGiftsGrantsEtcAmt",
            "//Return/ReturnData/IRS990EZ/ContributionsGiftsGrantsEtc",
        ],
        "program_service_revenue": [
            "//Return/ReturnData/IRS990EZ/ProgramServiceRevenueAmt",
            "//Return/ReturnData/IRS990EZ/ProgramServiceRevenue",
        ],
        "investment_income": [
            "//Return/ReturnData/IRS990EZ/InvestmentIncomeAmt",
            "//Return/ReturnData/IRS990EZ/InvestmentIncome",
        ],
    },
    "990PF": {
        "total_revenue": [
            "//Return/ReturnData/IRS990PF/TotalRevAndExpnssAmt",
            "//Return/ReturnData/IRS990PF/TotalRevenueAndExpenses/RevenueAndExpensesPerBks",
            "//Return/ReturnData/IRS990PF/AnalysisOfRevenueAndExpenses/TotalRevAndExpnssAmt",
        ],
        "total_expenses": [
            "//Return/ReturnData/IRS990PF/TotalExpensesRevAndExpnssAmt",
            "//Return/ReturnData/IRS990PF/AnalysisOfRevenueAndExpenses/TotalExpensesRevAndExpnssAmt",
        ],
        "net_assets": [
            "//Return/ReturnData/IRS990PF/TotNetAstOrFundBalancesEOYAmt",
            "//Return/ReturnData/IRS990PF/TotalNetAssetsFundBalances/EOY",
        ],
        "contributions_and_grants": [
            "//Return/ReturnData/IRS990PF/ContriRcvdRevAndExpnssAmt",
            "//Return/ReturnData/IRS990PF/AnalysisOfRevenueAndExpenses/ContriRcvdRevAndExpnssAmt",
        ],
        "investment_income": [
            "//Return/ReturnData/IRS990PF/InvstIncmRevAndExpnssAmt",
            "//Return/ReturnData/IRS990PF/AnalysisOfRevenueAndExpenses/InvstIncmRevAndExpnssAmt",
        ],
    },
}

PERSON_XPATHS = {
    "container": [
        "//Return/ReturnData/IRS990/Form990PartVIISectionAGrp",
        "//Return/ReturnData/IRS990/Form990PartVIISectionA",
    ],
    "name": ["PersonNm", "PersonName/PersonFirstName"],
    "title": ["TitleTxt", "Title"],
    "compensation": [
        "ReportableCompFromOrgAmt",
        "ReportableCompensationAmt",
        "Compensation",
    ],
    "is_officer": ["OfficerInd", "Officer"],
    "is_director": ["IndividualTrusteeOrDirectorInd", "IndividualTrusteeOrDirector"],
    "is_key_employee": ["KeyEmployeeInd", "KeyEmployee"],
    "is_highest_compensated": [
        "HighestCompensatedEmployeeInd",
        "HighestCompensatedEmployee",
    ],
}

GRANT_XPATHS = {
    "container": [
        "//Return/ReturnData/IRS990PF/SupplementaryInformationGrp/GrantOrContributionPdDurYrGrp",
        "//Return/ReturnData/IRS990PF/SupplementaryInformation/GrantOrContributionPdDurYr",
    ],
    "recipient_name": [
        "RecipientPersonNm",
        "RecipientBusinessName/BusinessNameLine1Txt",
        "RecipientBusinessName/BusinessNameLine1",
    ],
    "recipient_city": ["RecipientUSAddress/CityNm", "RecipientUSAddress/City"],
    "recipient_state": [
        "RecipientUSAddress/StateAbbreviationCd",
        "RecipientUSAddress/State",
    ],
    "amount": ["Amt", "Amount"],
    "purpose": ["GrantOrContributionPurposeTxt", "PurposeOfGrantOrContribution"],
}

# Integer fields vs text fields
INT_FIELDS = {
    "total_revenue",
    "total_expenses",
    "net_assets",
    "contributions_and_grants",
    "program_service_revenue",
    "investment_income",
    "program_expenses",
    "management_expenses",
    "fundraising_expenses",
    "num_employees",
    "num_volunteers",
}

TEXT_FIELDS = {"mission_description"}


# --- Dataclasses ---


@dataclass
class ParsedPerson:
    name: str
    title: str | None = None
    compensation: int | None = None
    is_officer: bool = False
    is_director: bool = False
    is_key_employee: bool = False
    is_highest_compensated: bool = False


@dataclass
class ParsedGrant:
    recipient_name: str
    recipient_ein: str | None = None
    recipient_city: str | None = None
    recipient_state: str | None = None
    amount: int | None = None
    purpose: str | None = None


@dataclass
class ParsedFiling:
    ein: str
    name: str
    city: str | None = None
    state: str | None = None
    tax_year: int | None = None
    form_type: str | None = None
    total_revenue: int | None = None
    total_expenses: int | None = None
    net_assets: int | None = None
    contributions_and_grants: int | None = None
    program_service_revenue: int | None = None
    investment_income: int | None = None
    program_expenses: int | None = None
    management_expenses: int | None = None
    fundraising_expenses: int | None = None
    num_employees: int | None = None
    num_volunteers: int | None = None
    mission_description: str | None = None
    people: list[ParsedPerson] = field(default_factory=list)
    grants: list[ParsedGrant] = field(default_factory=list)


# --- Helpers ---


def _strip_namespace(root):
    """Remove XML namespace prefixes for easier XPath queries."""
    for elem in root.iter():
        if elem.tag and isinstance(elem.tag, str) and "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]
        # Also strip namespace from attributes
        new_attrib = {}
        for key, val in elem.attrib.items():
            if "}" in key:
                key = key.split("}", 1)[1]
            new_attrib[key] = val
        elem.attrib.clear()
        elem.attrib.update(new_attrib)


def _extract_text(root, xpaths: list[str]) -> str | None:
    """Try each XPath and return the first non-empty text value."""
    for xpath in xpaths:
        elements = root.xpath(xpath)
        if elements:
            text = elements[0].text
            if text and text.strip():
                return text.strip()
    return None


def _extract_int(root, xpaths: list[str]) -> int | None:
    """Try each XPath and return the first non-None int value."""
    text = _extract_text(root, xpaths)
    if text is None:
        return None
    try:
        return int(text)
    except (ValueError, TypeError):
        return None


def _extract_bool(element, tag_names: list[str]) -> bool:
    """Check if any of the tag names have a truthy value in the element."""
    for tag in tag_names:
        found = element.xpath(tag)
        if found:
            text = found[0].text
            if text and text.strip().upper() in ("X", "1", "TRUE", "YES"):
                return True
    return False


# --- Main parser ---


def parse_filing(xml_bytes: bytes) -> ParsedFiling | None:
    """Parse an IRS 990 XML filing into a ParsedFiling dataclass.

    Returns None for malformed or unparseable XML.
    """
    if not xml_bytes:
        return None

    try:
        root = _safe_fromstring(xml_bytes)
    except (XMLSyntaxError, ValueError) as exc:
        logger.warning("Failed to parse XML: %s", exc)
        return None

    _strip_namespace(root)

    # Extract header info
    ein = _extract_text(root, HEADER_XPATHS["ein"])
    name = _extract_text(root, HEADER_XPATHS["name"])

    if not ein or not name:
        logger.warning("Missing EIN or name in filing")
        return None

    city = _extract_text(root, HEADER_XPATHS["city"])
    state = _extract_text(root, HEADER_XPATHS["state"])
    tax_year = _extract_int(root, HEADER_XPATHS["tax_year"])
    form_type = _extract_text(root, HEADER_XPATHS["form_type"])

    # Determine which field map to use
    field_map_key = form_type if form_type in FIELD_MAPS else "990"
    field_map = FIELD_MAPS[field_map_key]

    # Extract financial fields
    kwargs: dict = {}
    for field_name, xpaths in field_map.items():
        if field_name in INT_FIELDS:
            kwargs[field_name] = _extract_int(root, xpaths)
        else:
            kwargs[field_name] = _extract_text(root, xpaths)

    # Extract people (990 only)
    people: list[ParsedPerson] = []
    if form_type == "990":
        people = _extract_people(root)

    # Extract grants (990PF only)
    grants: list[ParsedGrant] = []
    if form_type == "990PF":
        grants = _extract_grants(root)

    return ParsedFiling(
        ein=ein,
        name=name,
        city=city,
        state=state,
        tax_year=tax_year,
        form_type=form_type,
        people=people,
        grants=grants,
        **kwargs,
    )


def _extract_people(root) -> list[ParsedPerson]:
    """Extract officers/directors/key employees from a 990 filing."""
    people: list[ParsedPerson] = []

    for xpath in PERSON_XPATHS["container"]:
        containers = root.xpath(xpath)
        if containers:
            for person_elem in containers:
                person_name = _extract_text(
                    person_elem, PERSON_XPATHS["name"]
                )
                if not person_name:
                    continue

                title = _extract_text(person_elem, PERSON_XPATHS["title"])

                comp_text = _extract_text(
                    person_elem, PERSON_XPATHS["compensation"]
                )
                compensation = None
                if comp_text:
                    with contextlib.suppress(ValueError, TypeError):
                        compensation = int(comp_text)

                people.append(
                    ParsedPerson(
                        name=person_name,
                        title=title,
                        compensation=compensation,
                        is_officer=_extract_bool(
                            person_elem, PERSON_XPATHS["is_officer"]
                        ),
                        is_director=_extract_bool(
                            person_elem, PERSON_XPATHS["is_director"]
                        ),
                        is_key_employee=_extract_bool(
                            person_elem, PERSON_XPATHS["is_key_employee"]
                        ),
                        is_highest_compensated=_extract_bool(
                            person_elem,
                            PERSON_XPATHS["is_highest_compensated"],
                        ),
                    )
                )
            break  # Use first matching container XPath

    return people


def _extract_grants(root) -> list[ParsedGrant]:
    """Extract grants from a 990-PF filing."""
    grants: list[ParsedGrant] = []

    for xpath in GRANT_XPATHS["container"]:
        containers = root.xpath(xpath)
        if containers:
            for grant_elem in containers:
                recipient_name = _extract_text(
                    grant_elem, GRANT_XPATHS["recipient_name"]
                )
                if not recipient_name:
                    continue

                amount_text = _extract_text(
                    grant_elem, GRANT_XPATHS["amount"]
                )
                amount = None
                if amount_text:
                    with contextlib.suppress(ValueError, TypeError):
                        amount = int(amount_text)

                grants.append(
                    ParsedGrant(
                        recipient_name=recipient_name,
                        recipient_city=_extract_text(
                            grant_elem, GRANT_XPATHS["recipient_city"]
                        ),
                        recipient_state=_extract_text(
                            grant_elem, GRANT_XPATHS["recipient_state"]
                        ),
                        amount=amount,
                        purpose=_extract_text(
                            grant_elem, GRANT_XPATHS["purpose"]
                        ),
                    )
                )
            break  # Use first matching container XPath

    return grants
