
import knowledge_store as knowledge



from fastapi import APIRouter,HTTPException, Header, Depends

from documents import DOCUMENTS 
from pydantic import BaseModel ,Field


from fastapi.responses import StreamingResponse

import llm
from llm import stream_grounded_answer

router = APIRouter(prefix="/knowledge",tags=["knowledge"])




#USING RELEVENCE FLOOR TO STOP LLM CALL IF DOCUMENTS DONT MEET THRESHOLD OF RELEVENCE TO THE QUERY/QUESTION
RELEVENCE_FLOOR = 0.4







# class (QUESTION) using base model with 2 field (question and top_k)
class Question(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=3, gt=0,le=8) 



#use prefix knowledge in curl to run - 
#it is POST becuase POST creates something but at higher level POST does something (not like get) - like action

@router.post("/index")
def rebuild_index():
    """Embed the corpus. Costs tokens....so it is a deliberate POST,rather than automatic"""
    tokens =  knowledge.build_index()
    return {"indexed": knowledge.count(), "embedding_tokens": tokens}


@router.post("/search")
def search(q: Question)->dict:
    """RETRIVES TOP K DOCUMENTS IN SEMENTIC SEARCH FROM VECTOR DATABASE + SCORES OF EACH """
    response = knowledge.search(q.question,q.top_k)
    return {"results":response}



# curl command for testing 

# curl -X POST "http://127.0.0.1:8000/knowledge/search"   -H "Content-Type: application/json"   -d '{"question": "What is Linda'\''s Portfolio","top_k": 3}'





# MAIN FEATUERE ENDPOINT - Client portfolio input   - GROUNDED  Stream Summary  of which fund best 
# Asks from grounded search 
#search + groiunded
@router.post("/ask")
def stream_grounded_answer(q: Question)->dict:  
    """RETRIVES TOP 3 DOCUMENTS OF RELEVENCE FROM SEARCH , THE CALLS LLM TO ANSWER SEARCH WITH GROUNDED ANSWER"""

    # 1. Retrieve
    #same call as "/knowledge/search "
    try:
        hits = knowledge.search( q.question, q.top_k ) 
    except RuntimeError as e:
        raise HTTPException(status_code=409, detail=str(e) ) 


    
    # 2. Filter, and decide whether to make a call to the model at all
    # (compare against our RELEVENCE_FLOOR )
    usable = [hit for hit in hits if hit["score"] >= RELEVENCE_FLOOR ]
    if not usable:
        return {
            "question": q.question,
            "answer": None,
            "refused": True,
            "reason": " No document in the corpus is relevent to that question.",
            "sources": []
        }

    
    #3.  Build context from relevent docs/hits , then call AI and generate the answer (not before)
    context = "\n\n".join(f"[{h['id']}] {h['title']}\n{h['Content']}" for h in usable)

    return StreamingResponse(
        llm.stream_grounded_answer(q.question, context),
        media_type="text/plain",
    )
















