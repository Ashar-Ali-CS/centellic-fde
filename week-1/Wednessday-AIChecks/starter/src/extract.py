"""Extract a monetary amount from a line of text, using a model.

LEARNER STARTER. SYNTHETIC PLACEHOLDER DATA ONLY.

This module currently does the naive thing. It runs. It is also untestable and
unsafe, in ways the three gates from Day 1 will only partly catch.
"""

import json

from typing import Any

from decimal import Decimal

from model_client import FakeModel,ModelClient


from pydantic import BaseModel,  field_validator

import re 



class ModelRefused(Exception):
    """ The model returned no JSOB object at all"""
    def __init__(self, reply: str) -> str:
        return (f"Model refused to return a JSON object. ")


class ModelContractViolation(Exception):
    """ The Model returned JSON that does not match the expected schema"""
    def __init__(self,reply:str) -> str:
        return (f"Model returned JSON that does not match the expected schema.")


class ModelReply(BaseModel):
    amount: Decimal
    @field_validator("amount", mode="before")
    @classmethod
    def reject_float(cls, value: object) -> object:
        if isinstance(value, float):
            raise ValueError(f"amount must arrive as a string ,not float")
        return value

def extract_amount(line:str, client: ModelClient) -> Decimal :
    """Ask the model for the amount in a line and return it."""
   
    reply = client.complete(f"What is the amount in this line? {line}")
 
    _JSON_OBJECT = re.compile(r"\{.*\}", re.DOTALL)

    match = _JSON_OBJECT.search(reply)
    if match is None:
        raise ModelRefused(reply.strip()[:200])
    try:
        return ModelReply.model_validate_json(match.group(0)).amount
    except ValidationError as error:
        raise ModelContractViolation(str(error.splitlines()[0]) from error)