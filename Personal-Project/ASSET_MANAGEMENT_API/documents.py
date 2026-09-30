

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
        "fund_id":1,
        "client_id":None,
        "type": "fund_factsheet",
        "body": (
            "Fund_Name: ManGuard Class C Fund " 
            "Fund_Strategy: "
            "Fund_Fees:  1 percent annual , No Exit Fees "
            "ESG: Sustainability only "
            "Risk_Rating: Low"
        ),
    },
    {
        "id": "doc-002",
        "title": "BlueRock - Class A Fund ",
        "fund_id":2,
        "client_id":None,
        "type": "fund_factsheet",
        "body": (
            "Fund_Name: BlueRock Class A Fund " 
            "Fund_Strategy: "
            "Fund_Fees:  5 percent annual  , 1 percent Exit Fees "
            "ESG: Sustainability, No Alchohol companies , No Tabacco companies "
            "Risk_Rating:Low"
        ),
    },
    {
        "id": "doc-003",
        "title": "FastSaver Pension Fund ",
        "type": "fund_factsheet",
        "fund_id":3,
        "client_id":None,
        "body": (
            "Fund_Name: FastSaver Pension Fund  " 
            "Fund_Strategy:  unknown "
            "Fund_Fees:  5 percent annual  , 1 percent Exit Fees "
            "ESG: Sustainability, No Alchohol companies , No Tabacco companies "
            "Risk_Rating:Low"
        ),
    },
    {
        "id": "doc-004",
        "title": " Jenny BlueRock Manager - BlueRock is best option for sustainable investors. ",
        "type": "manager_commentry",
        "fund_id": None,
        "client_id":None,
        "body": (
            " At BlueRock our new class A fund is best option for investors who are focused on enviroment. Trust me "
        ),
    },
    {
        "id": "doc-005",
        "title": " Jane's Portfolio :)  ",
        "type": "client_portfolio",
        "fund_id": None,   
        "client_id":1, 
        "body": (
            "Client_Name: Jane Turncoat"
            "Portfolio_Breakdown: 50 percent-FastSaver pension fund, 15 percent-BlueRock class A fund , 35 percent-Other Assets  "
            "Total_assets: 500000"
            "Client_Mandate - No Tobacco, Sustainability focus"
        ),
    },
    {
        "id": "doc-006",
        "title": " Micheal's - Portfolio",
        "type": "client_portfolio",
        "fund_id": None,
        "client_id":2, 
        "body": (
            "Client_Name: Micheal Presly  "
            "Portfolio_Breakdown: 50 percent ManGuard class C fund , 50 percent FastSaver pension Fund "
            "Total_Assets: 100000"
            "Client_Mandate - No restrictions"
        ),
    },
    {
        "id": "doc-007",
        "title": " Sven's -Portfolio ",
        "type": "client_portfolio",
        "fund_id": None,
        "client_id":3, 
        "body": (
            "Client_Name: Sven Godwinson "
            "Portfolio_Breakdown:  50 percent FastSaver pension Fund,50 percent other assets "
            "Total_assets: 100000"
            "Client_Mandate - No restrictions"
        ),
    },
    {
        "id": "doc-008",
        "title": "",
        "type": "client_portfolio",
        "client_id":4, 
        "fund_id": None,
        "body": (
            "Client_Name: Linda Langstrom"
            "Portfolio_Breakdown: 100 percent ManGuard class C fund "
            "Total_assets: 123000"
            "Client_Mandate - No restrictions"
        ),
    },
    {
        "id": "doc-009",
        "title": " Victor Magnate, Senior portfolio manager - Pensioner's need a new way ",
        "type": "manager_commentry",
        "fund_id": None,
        "client_id":None,
        "body": (
            "Inflation is rising and  assets depreciate in values, At FastSaver, we realise that and have started a new pension fund for those trying to earn fast"
        ),
    },
    {
        "id": "doc-010",
        "title": " ManGuard Future fund  ",
        "type": "fund_factsheet",
        "fund_id": 4,
        "client_id":None,
        "body": (
            "Fund_Name: ManGuard Future Fund " 
            "Fund_Strategy: "
            "Fund_Fees: 0.1 percent annual, no exit fees "
            "ESG: None "
            "Risk_Rating:High"
        ),
    },

]