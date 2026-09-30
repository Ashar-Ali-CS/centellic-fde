

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

SYSTEM_PROMPT = (
    "You are a helpfull asset portfolio manager assistent. "
    "Use British English "
     
)


