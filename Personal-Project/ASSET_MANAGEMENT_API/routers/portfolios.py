


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




#Endpoint 2 - Get specific client_portfolio based on client id 

# curl http://127.0.0.1:8000/portfolios/2


@router.get("/{client_id}")
def get_client_portfolio( client_portfolio: dict = Depends(get_client_or_404)):
    return client_portfolio




#Endpoint for adding client portfolio plan, this is done by the manager. 
#They may want to make note of what the client 

#class NewPortfolio (BaseModel):
#      next doc 
#    title = ""
#    fund_id = 
#    client_id
#    body 


#post document based on verfication class
@router.post("NewPortfolio")
def add_client_portfolio( ):
    return ("IN PROGRESS")
    

#Changing client portfolio notes
#@router.put("/{client_id}")
#def update_firm(new:NewFirm,firm: dict = Depends(get_client_or_404)):
#    firm.update({
#        "name": new.name,
#        "jurisdiction": new.jurisdiction,
#        "revenue_usd_m": new.revenue_usd_m,
#        "lawyers": new.lawyers,
#        "equity_partners": new.equity_partners
#    })
 #   return firm 

