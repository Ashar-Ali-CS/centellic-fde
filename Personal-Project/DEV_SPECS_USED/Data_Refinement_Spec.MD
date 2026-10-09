

SPEC FOR REFINING SYNTHETIC DOCUMENTS FOR MY ASSET MANAGMENT PROJECT(FastAPI) 


Aim  - To refine my existing 10 documents in data , to make the prose more realistic to asset managment context. 




CONTEXT (the documents)

Types include:
Fund Factsheets - these include fund name ( FundCOMPANY Class C ), fund strategy, included fees,risk rating (standard deivation or other metric)

Manager commentry  - Notes by people/managmeners of the funds?

client portfolios -  this is for the client, has client_id  - what the client wants and ESG/client mandate

Here is existing documents for reference:



DOCUMENTS: list[dict[str, Any]] = [
    {
        "id": "doc-001",
        "title": " ManGuard Class C Fund ",
        "fund_id":1,
        "client_id": None,
        "type": "fund_factsheet",
        "body": (
            "Fund_Name: ManGuard Class C Fund / " 
            "Fund_Strategy: Unkown / "
            "Fund_Fees:  1 percent annual , No Exit Fees / "
            "ESG: Sustainability only / "
            "Risk_Rating: Low / "
        ),
    },
    {
        "id": "doc-002",
        "title": "BlueRock - Class A Fund ",
        "fund_id":2,
        "client_id": None,
        "type": "fund_factsheet",
        "body": (
            "Fund_Name: BlueRock Class A Fund, " 
            "Fund_Strategy: Unknown,  "
            "Fund_Fees:  5 percent annual , 1 percent Exit Fees, "
            "ESG: Sustainability, No Alchohol companies , No Tabacco companies, "
            "Risk_Rating:Low, "
        ),
    },
    {
        "id": "doc-003",
        "title": "FastSaver Pension Fund ",
        "type": "fund_factsheet",
        "fund_id":3,
        "client_id": None,
        "body": (
            "Fund_Name: FastSaver Pension Fund ,  " 
            "Fund_Strategy:  unknown,  "
            "Fund_Fees:  5 percent annual  , 1 percent Exit Fees,  "
            "ESG: Sustainability, No Alchohol companies , No Tabacco companies,  "
            "Risk_Rating:Low, "
        ),
    },
    {
        "id": "doc-004",
        "title": " Jenny, BlueRock Manager - BlueRock is best option for sustainable investors. ",
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
        "title": " Linda's Portfolio :)   ",
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



Rules 

- Only the 3 types of documents 

- Out of scope: "id" , "fund_id", "client_id", "type"

- Modify the body only. 

- Keep each document body under or equal 60 words 

- Consistent body structure for each client portfolio,like existing one but more realistic to how asset managment system would be 

- Consistent body structure/format for each fund fact sheet ,like existing one but more realistic to how asset managment system would be 

- Manager commentry realistic 







 Tasks 

 1. Look through existing 10 documents , give me your opinon and ask me questions if you have before generation


 2. Generete the refined more realistic prose for  DOCUMENTS

 
 Complete task 1 NOW




 (NOTE -  I prompted GPT-5.6 Luna with this spec, it made it more realistic fees and other things like risk rating - in some parts i changed the "%" to percent as it was red) 


