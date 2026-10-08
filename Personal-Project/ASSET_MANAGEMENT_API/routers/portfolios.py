


from fastapi import APIRouter,HTTPException, Header, Depends

from documents import DOCUMENTS 
from pydantic import BaseModel ,Field


router = APIRouter(prefix="/portfolios",tags=["portfolios"])




#this is helper function to search for the client_id 
def get_client_or_404(client_id: int) -> dict:
    for document in DOCUMENTS:
        if document["client_id"] == client_id:
            return document
    raise HTTPException(status_code=404, detail=f"No portfolio  with client_id {client_id} found")




#this is for idempotency of POST (adding client portfolio)
#avoids duplication - same outcome ,no matter how many times 

_seen_keys: dict[str, dict] = {}




#Endpoint 1 - Get specific client_portfolio based on client id 

# curl http://127.0.0.1:8000/portfolios/2


@router.get("/{client_id}")
def get_client_portfolio( client_portfolio: dict = Depends(get_client_or_404)):
    return client_portfolio





#This is pydantic verifcation/validation model for posting and changing client portfolios
#Pydantic validation for posting/adding new client portfolio and change/put
class NewPortfolio(BaseModel):
    #title,body
    title: str = Field(..., example="Ashar's portfolio")
    body: str = Field(..., example="Client_Name: Ashar Ali...")
    


#Endpoint2 - for adding client portfolio plan, this is done by the manager. 
#post document based on verfication class
#portfolios/add
@router.post("/add")
def add_client_portfolio(new:NewPortfolio, idempotency_key:str | None = Header(default=None )):
    """ ADDING/POSTING NEW CLIENT PORTFOLIO , OPTIONAL IDEMPOTENCY TO STOP DUPLICATES. 
     IMPORTANT: FOR THE BODY OF CLIENT PORTFOLIO ,THE MANAGER JUST HAS TO FOLLOW FORMAT - 
     Client_Name: ... Portfolio_Breakdown: ... Total_assets: ... Client_Mandate - ..."""
    if idempotency_key is not None and idempotency_key in _seen_keys:
        return _seen_keys[idempotency_key]

    # Generate new doc ID cleanly
    new_doc_id = f"doc-{len(DOCUMENTS) + 1:03d}"

    #  creates client_id for new portfolio
    #  by finding the current highest client_id
    existing_client_ids = [
        doc["client_id"] for doc in DOCUMENTS 
        if doc.get("client_id") is not None
    ]
    next_client_id = max(existing_client_ids, default=0) + 1



    client_portfolio = {
        "id": new_doc_id,
        "title": new.title,
        "type": "client_portfolio",
        "fund_id": None,
        "client_id": next_client_id,
        "body": new.body,
    }
    DOCUMENTS.append(client_portfolio)

    if idempotency_key is not None:
        _seen_keys[idempotency_key]=client_portfolio
    return client_portfolio


# Endpoint 3 - Edit existing client portfolios

@router.put("/edit/{client_id}")
def edit_portfolio(new:NewPortfolio,client_portfolio: dict = Depends(get_client_or_404)):
    """CHANGEING EXISTING CLIENT PORTFOLIO BY CLIENT ID
     IMPORTANT: FOR THE BODY OF CLIENT PORTFOLIO ,THE MANAGER JUST HAS TO FOLLOW FORMAT - 
     Client_Name: ... Portfolio_Breakdown: ... Total_assets: ... Client_Mandate - ..."""
    client_portfolio.update({
        "title": new.title,
        "body": new.body,
        
    })
    return client_portfolio




# ENDPOINT 4 - DELETE 
@router.delete("/{client_id}", status_code=204)
def delete_portfolio(client_portfolio: dict = Depends(get_client_or_404)):
    """REMOVES CLIENT PORTFOLIO BY CLIENT ID"""
    DOCUMENTS.remove(client_portfolio)
    return











