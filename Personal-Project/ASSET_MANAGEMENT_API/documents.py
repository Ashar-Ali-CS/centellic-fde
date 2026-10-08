

"""     

 SYNTHETIC PLACEHOLDER DATA FOR ASSET AND WEALTH MANAGMENT SYSTEM "
this holds prose - the kind of unstructured text a client would actually have .
None of this data is real.

Types include:
Fund Factsheets - these include fund name ( FundCOMPANY Class C ), fund strategy, included fees,risk rating (standard deivation or other metric)

Manager commentry  - Notes by people/managmeners of the funds?

client portfolios -  this is for the client, has client_id  - what the client wants and ESG/client mandate

"""

from typing import Any

#fund id   ,if its fund
#client id if its client portfolio note. 

DOCUMENTS: list[dict[str, Any]] = [
    {
        "id": "doc-001",
        "title": " ManGuard Class C Fund ",
        "fund_id": 1,
        "client_id": None,
        "type": "fund_factsheet",
        "body": (
            "Fund_Name: ManGuard Class C Fund / "
            "Fund_Strategy: Diversified multi-asset strategy investing primarily in investment-grade bonds and defensive equities / "
            "Fund_Fees: Annual Management Fee 0.75%, Exit Fee 0% / "
            "ESG: Sustainability considerations integrated into security selection / "
            "Risk_Rating: Low (2/7)"
        ),
    },
    {
        "id": "doc-002",
        "title": "BlueRock - Class A Fund ",
        "fund_id": 2,
        "client_id": None,
        "type": "fund_factsheet",
        "body": (
            "Fund_Name: BlueRock Class A Fund / "
            "Fund_Strategy: Global equity strategy focused on companies demonstrating strong environmental practices and long-term sustainable growth / "
            "Fund_Fees: Annual Management Fee 0.85%, Exit Fee 1% / "
            "ESG: Excludes tobacco and alcohol producers; sustainability-focused mandate / "
            "Risk_Rating: Moderate (4/7)"
        ),
    },
    {
        "id": "doc-003",
        "title": "FastSaver Pension Fund ",
        "type": "fund_factsheet",
        "fund_id": 3,
        "client_id": None,
        "body": (
            "Fund_Name: FastSaver Pension Fund / "
            "Fund_Strategy: Diversified growth strategy designed for long-term pension investing, with exposure to global equities and fixed income / "
            "Fund_Fees: Annual Management Fee 0.65%, Exit Fee 1% / "
            "ESG: Excludes tobacco and alcohol producers; sustainability considerations applied / "
            "Risk_Rating: Moderate (4/7)"
        ),
    },
    {
        "id": "doc-004",
        "title": " Jenny, BlueRock Manager - BlueRock is best option for sustainable investors. ",
        "type": "manager_commentry",
        "fund_id": None,
        "client_id": None,
        "body": (
            "Manager: Jenny, BlueRock Fund Manager / "
            "Commentary: BlueRock's sustainability-focused equity strategy remains attractive for investors seeking long-term growth alongside environmental considerations. "
            "Recent portfolio positioning favours companies with improving sustainability practices and resilient business models. "
            "Market volatility remains a key risk, particularly for higher-growth holdings."
        ),
    },
    {
        "id": "doc-005",
        "title": " Jane's Portfolio :)  ",
        "type": "client_portfolio",
        "fund_id": None,
        "client_id": 1,
        "body": (
            "Client_Name: Jane Turncoat / "
            "Portfolio_Allocation: 50 percent FastSaver Pension Fund; 15 percent BlueRock Class A Fund; 35 percent Other Assets / "
            "Total_Assets: £500,000 / "
            "Client_Mandate: Sustainability focus; no tobacco exposure"
        ),
    },
    {
        "id": "doc-006",
        "title": " Micheal's - Portfolio",
        "type": "client_portfolio",
        "fund_id": None,
        "client_id": 2,
        "body": (
            "Client_Name: Michael Presly / "
            "Portfolio_Allocation: 50 percent ManGuard Class C Fund; 50 percent FastSaver Pension Fund / "
            "Total_Assets: £100,000 / "
            "Client_Mandate: No specific investment or ESG restrictions"
        ),
    },
    {
        "id": "doc-007",
        "title": " Sven's -Portfolio ",
        "type": "client_portfolio",
        "fund_id": None,
        "client_id": 3,
        "body": (
            "Client_Name: Sven Godwinson / "
            "Portfolio_Allocation: 50 percent FastSaver Pension Fund; 50 percent Other Assets / "
            "Total_Assets: £100,000 / "
            "Client_Mandate: No specific investment or ESG restrictions"
        ),
    },
    {
        "id": "doc-008",
        "title": " Linda's Portfolio :)   ",
        "type": "client_portfolio",
        "client_id": 4,
        "fund_id": None,
        "body": (
            "Client_Name: Linda Langstrom / "
            "Portfolio_Allocation: 100% ManGuard Class C Fund / "
            "Total_Assets: £123,000 / "
            "Client_Mandate: No specific investment or ESG restrictions"
        ),
    },
    {
        "id": "doc-009",
        "title": " Victor Magnate, Senior portfolio manager - Pensioner's need a new way ",
        "type": "manager_commentry",
        "fund_id": None,
        "client_id": None,
        "body": (
            "Manager: Victor Magnate, Senior Portfolio Manager / "
            "Commentary: FastSaver is positioned for investors seeking long-term pension growth rather than short-term returns. "
            "The fund maintains diversified exposure across equities and fixed income to manage market risk. "
            "Persistent inflation and changes in interest rates remain important considerations for the portfolio's future performance."
        ),
    },
    {
        "id": "doc-010",
        "title": " ManGuard Future fund  ",
        "fund_id": 4,
        "client_id": None,
        "type": "fund_factsheet",
        "body": (
            "Fund_Name: ManGuard Future Fund / "
            "Fund_Strategy: High-growth equity strategy investing primarily in emerging technology and innovative companies / "
            "Fund_Fees: Annual Management Fee 0.50%, Exit Fee 0% / "
            "ESG: No specific ESG exclusions or sustainability mandate / "
            "Risk_Rating: High (6/7)"
        ),
    },
]