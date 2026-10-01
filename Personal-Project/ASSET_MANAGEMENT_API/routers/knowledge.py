
import knowledge_store as knowledge



from fastapi import APIRouter,HTTPException, Header, Depends

from documents import DOCUMENTS 
from pydantic import BaseModel ,Field


router = APIRouter(prefix="/knowledge",tags=["knowledge"])




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
    response = knowledge.search(q.question,q.top_k)
    return {"results":response}



#testing 

# curl -X POST http://127.0.0.1:8000/knowledge/search -H "Content-Type: application/json" \ -d '{"question":"Which firms operate in the United States?"}'


