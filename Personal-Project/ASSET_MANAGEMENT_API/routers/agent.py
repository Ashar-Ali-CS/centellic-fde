



from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

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
    """Ask agent question - streams the response back chunk by chunk."""
    try:
        # Assuming your agent can yield text chunks or you have a streaming version of ask_with_tools
        def generate():
            # If your agent function supports yielding chunks:
            for chunk in agent.ask_with_tools(question):
                yield chunk
                
        return StreamingResponse(generate(), media_type="text/plain")
        
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="AI Agent timed out")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="AI Agent rate limited")
    except APIStatusError:
        raise HTTPException(status_code=502, detail="AI Agent unavailable")