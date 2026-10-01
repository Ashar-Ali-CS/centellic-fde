

#how we call the model (nothing knows about fastapi )

#api burnt at end of day 
#dont close (set on session)

import os
import anthropic

from anthropic import APIStatusError, APITimeoutError,RateLimitError

from pydantic import BaseModel, Field

import time

MODEL = "claude-haiku-4-5-20251001"

#the sdk defualt are max retry 2 ,600 second timeout
#overwritten here as descision

client = anthropic.Anthropic(
    api_key = os.environ["ANTHROPIC_API_KEY"],
    timeout=30.0,
    max_retries=3,

)


#the prompt and where the rules live 

#RULES GO IN SYSTEM
#DATA GOES IN USER 




#-----------------------LLM summmary for summary of fund facts---------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a helpfull asset portfolio manager assistent. "
    "Use British English "
    "  ??? "
     
)


#this function is too build the prompt used to summarise fund fact sheets by fund id 
def build_prompt( fund_factsheet:dict) -> str:
    return (
        f"Summarise this investment fund factsheet for a portfolio manager in formal yet fun way"
        f"Name: {fund_factsheet["title"]} "
        f"Body:{fund_factsheet["body"]} "
    )


#
def summarise_fund_factsheet(fund_factsheet:dict) -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(fund_factsheet)}],
    )
    return {
        "id":fund_factsheet["fund_id"],
        "name": fund_factsheet["title"],
        "summary": response.content[0].text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "stop_reason": response.stop_reason,
    }



#-----------------------LLM analysis of client portfolios---------------------------------------------------------------------





#this function is too build the prompt used to summarise fund fact sheets by fund id 
def build_prompt( fund_factsheet:dict) -> str:
    return (
        f"Analyse this investment fund factsheet for a portfolio manager in formal but fun way"
        f"Name: {fund_factsheet["title"]} "
        f"Body:{fund_factsheet["body"]} "
    )



class PortfolioAnalysis(BaseModel):
    """validation- The shape of analysis we  require back,it is not suggestion to model ,it is a contract""" 
    #
    # strengths 
    strengths: list[str] = Field(max_length=3)
    # risks 
    risks: list[str] = Field(max_length=3)
    # #headcount_effeciency 
    



def portfolio_analysis(client_portfolio: dict) -> dict:
    """Structured output. The response is validated against the FirmAnalsyis... or it fails """
    response = client.messages.parse(
        model=MODEL,
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_portfolio_prompt(client_portfolio)}],
        output_format=PortfolioAnalysis, 
    )

    #not free text returned ?based on schema 
    analysis = response.content[0].parsed_output

    return {
        "id":client_portfolio["client_id"],
        "name": client_portfolio["title"],
        "analysis": analysis,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "stop_reason": response.stop_reason,
    }






#-----------------------RETRIEVEL AUGEMENTED RESPONSES FOR NEW CLIENT PORTFOLIO QUERYS LLM -------------------------------------




