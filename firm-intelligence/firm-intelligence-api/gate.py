
"""

The relevence gate - does a retrieved chunk deserve to reach the model ?

Each hit is judged by score that is ranked by:
    - a hit from azure carries rerank score (0-4 from the semantic reranker)
    - a hit from the local index carries only a cosine simalrity in 

A hit holding the same number/identifier as the question(exact_match) always passes. 


.venv/Scripts/python.exe -m pip install azure-search-documents==12.0.0 azure-identity==1.26.0

"""


#can set up parralel azure search or do ordinary way 

def is_usable(hit: dict,cosine_floor:float, rerank_floor:float) -> bool:
    if hit.get("exact_match", False):
        return True

    if hit.get("reranker_score") is not None:
        return hit["rerank_score"] >= rerank_floor
    
    return hit["score"] >= cosine_floor



