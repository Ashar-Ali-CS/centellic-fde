



from fastapi import APIRouter, HTTPException


from anthropic import APIStatusError, APITimeoutError, RateLimitError
import agent_settings as agent


router = APIRouter(prefix = "/agent", tags=["agent"])



#@router.post("/ask")
#def ask(question:str):
#    """ask agent question - it uses search with knowledge base or predict portfolio returns tool."""
#    try:
#        result = agent.ask_with_tools(question)
#        return result 
#    except APITimeoutError:
#            raise HTTPException(status_code=504, detail="AI Agent  timed out")
#    except RateLimitError:
#        raise HTTPException(status_code=429, detail="AI Agent rate limited")
#    except APIStatusError:
#        raise HTTPException(status_code=502, detail="AI Agent  unavailable")


# STREAMING VERSION IS CHOSEN 
@router.post("/ask")
def ask(question: str):
    """Ask agent question - returns a clean JSON dictionary."""
    try:
        # This must return a dictionary containing keys like:
        # answer, completed, tool_calls_made, input_tokens, output_tokens, stop_reason
        result = agent.ask_with_tools(question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))