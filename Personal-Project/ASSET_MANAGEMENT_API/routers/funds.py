




from fastapi import APIRouter,HTTPException, Header, Depends

from documents import DOCUMENTS 
from pydantic import BaseModel ,Field


router = APIRouter(prefix="/funds",tags=["funds"])


#Later for idemopotency 
_seen_keys: dict[str, dict] = {}





#this is helper function to search for the firm 
def get_fund_or_404(fund_id: int) -> dict:
    for document in DOCUMENTS:
        if document["fund_id"] == fund_id:
            return document
    raise HTTPException(status_code=404, detail=f"No fund factsheet  with fund id {fund_id} found")





# ASSET ENDPOINTS 


#ENDPOINT 1  -  Get all documents (fund fact sheets as well )
# curl http://127.0.0.1:8000/funds

@router.get("")
def list_fund_documents():
    return ( document for document in DOCUMENTS)


#Endpoint 2 - Get specific fund_fact sheet based on fund id 

@router.get("/{fund_id}")
def get_fact_sheet( fund_facts: dict = Depends(get_fund_or_404)):
    return fund_facts
    

#Endpoint 3 -  LLM Stream summary 







