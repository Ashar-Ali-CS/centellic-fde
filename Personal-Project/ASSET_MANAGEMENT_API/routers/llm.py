


from fastapi import APIRouter,HTTPException, Header, Depends

from documents import DOCUMENTS 
from pydantic import BaseModel ,Field

from anthropic import APIStatusError, APITimeoutError,RateLimitError

from fastapi.responses import StreamingResponse


import  llm 
from llm import MODEL, SYSTEM_PROMPT, build_prompt,build_portfolio_prompt , client
router = APIRouter(prefix="/llm",tags=["llm"])

RELEVENCE_FLOOR: 0.40




#I HAD PROBLEM WITH IMPORTNING THESE HELPER FUNCTIONS FROM THE funds.py and portfolios.py (server didnt understand)

#this is helper function to search for the firm 
def get_fund_or_404(fund_id: int) -> dict:
    for document in DOCUMENTS:
        if document["fund_id"] == fund_id:
            return document
    raise HTTPException(status_code=404, detail=f"No fund factsheet  with fund id {fund_id} found")

#this is helper function to search for the client_id 
def get_client_or_404(client_id: int) -> dict:
    for document in DOCUMENTS:
        if document["client_id"] == client_id:
            return document
    raise HTTPException(status_code=404, detail=f"No portfolio  with client_id {client_id} found")



#test returns sting working(no llm call)
@router.get("/test")
def test():
    return "WORKING"



# Endpoint 1 -formal summary  of fund_fact sheets by fund id or 404


# curl -X POST "http://127.0.0.1:8000/llm/summary/1" 

#The Call (reurns response.content[0].text which has response)
@router.post("/summary/{fund_id}")
def summary(fund_factsheet =Depends(get_fund_or_404)) -> dict:
    try:
        return llm.summarise_fund_factsheet(fund_factsheet)
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="Summary provider timed out")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Summary provider rate limited")
    except APIStatusError:
        raise HTTPException(status_code=502, detail="Summary provider unavailable")




# Endpoint 2 - variant of summary endpoint that streams the resposne
@router.post("/stream_summary/{fund_id}")
def get_stream_summary(fund_factsheet =Depends(get_fund_or_404)):
    try:
        return llm.stream_summary(fund_factsheet)
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="Summary provider timed out")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Summary provider rate limited")
    except APIStatusError:
        raise HTTPException(status_code=502, detail="Summary provider unavailable")





# Endpoint 3 - analysis of existing  client portfolio existing by client_id and reccomandaitions 


@router.post("/analyse/{client_id}")
def analyse(client_portfolio = Depends(get_client_or_404)) -> dict:
    try:
        return llm.portfolio_analysis(client_portfolio)
    except APITimeoutError:
        raise HTTPException(status_code=504, detail= "Analysis provider timed out")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Analysis provider rate limited")
    except APIStatusError:
        raise HTTPException(status_code=502, detail="Analysis provider unavailable")
    

    