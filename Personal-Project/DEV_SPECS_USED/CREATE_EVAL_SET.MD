SPEC FOR CREATING AN EVAL SET TO EVALUATE CHUNKING 


Aim  - To create an eval set for my documents following a specific format ,so that i can evalute optimal relevence floor and chunking strategy. 




CONTEXT (the documents)


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




eval set goes here:

"""A labelled eval set for retrieval and answer quality.

Each answerable question records:
  doc_id    the document that holds the answer
  evidence  a short verbatim span from that document. A retrieved chunk counts as a hit
            only if it contains this exact span, so a chunk that cuts the span in half
            is a miss. That is deliberate: it is how chunking damage shows up in the numbers.
  keywords  what a correct answer must mention. Every item must appear in the answer.
            "a|b" means either a or b is acceptable. Matching is case-insensitive and
            whole-word, so "no" does not match inside "not". A trailing * allows any
            ending, so "exclud*" matches "excluded" and "excludes". A refusal never
            counts as correct, whatever words it happens to contain.
  kind      what the question tests

Unanswerable questions have doc_id None and no evidence. The correct behaviour is refusal.
"""

EVAL_SET = [
    
]


def answerable() -> list[dict]:
    return [q for q in EVAL_SET if q["doc_id"] is not None]


def unanswerable() -> list[dict]:
    return [q for q in EVAL_SET if q["doc_id"] is None]









Rules 

-  Must follow the format

- Include 2/3 unanswerable queries 

- Must be answerable from provided docs 

- Tell me how many answerable and non answerable there are. 


 Tasks 

 1. Ask me if anything unclear before 


 2. Generate EVAL SET 


 
 Complete task 1 NOW




 (NOTE -  I will prompt GPT-5.6 Luna ) 


