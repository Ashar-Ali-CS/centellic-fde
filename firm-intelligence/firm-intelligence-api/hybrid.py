
"""
Hybrid search: vector search and keyword search , merged by rank. 

"""

from functools import lru_cache

import bm25
import chunk_index 
import chunking 

import fusion 
"""THIS FUNCTION IS FROM FUSION.PY - It didnt recorginse it as attribute of fusion"""
def reciprocal_rank_fusion(rankings: list[list[str]], k: int = 60) -> list[tuple[str,float]]:
    scores:dict[str, float] = {}
    for ranking in rankings: 
        for position, item in enumerate(ranking, start=1):
            scores[item] = scores.get(item,0.0) + 1.0 / (k + position)
    # ties keep the order the ids were added 
    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)

    # each judge gives a card 1 / (k + position) points... position 1 is the top of that judges list 

import re 

POOL = 10 

# 3 helpers 
#  1 big function 


# keyword_index

#(but need to restart server when change documents)
@lru_cache(maxsize=None)  #tells it to remember answer 
def keyword_index(strategy):
    return bm25.BM25Index(chunking.chunk_corpus(chunk_index.ALL_DOCUMENTS, strategy))


# identifiers 
def identifiers(text):
    return {token for token in bm25.tokenize(text) if any(ch.isdigit() for ch in token)}



# is_uasble 
    # this is our gate , in one line 
        # pass if cosine reach the floor OR the chunk shares a number with the question
def is_usable(hit,floor):
    return hit["score"] >= floor or hit.get("exact_match", False)



#our main function 
def search_with_vector(strategy: str, question: str, query_vector: list[float], top_k: int = 3, pool: int=POOL) -> list[dict]:
    """The top_k chunks for a question, found by vector search, keyword search or both """
    
    #ask both searchers 
    vector_hits = chunk_index.search_with_vectors(strategy, [query_vector], k=pool)[0]
    keyword_hits = keyword_index(strategy).search(question, k=pool)

    # merge with (reciprocal rank fusion) RRF, keep the top 3 
    # RFF only needs ids in order....pass 2 lists of ids and drop the scores (id,rrf_score)
    fused = reciprocal_rank_fusion([
        [hit["chunk_id"] for hit in vector_hits],
        [hit["chunk"]["id"] for hit in keyword_hits], 
    ])[:top_k]

    #make two look up tables 
    by_vector = {hit["chunk_id"]: hit for hit in vector_hits}
    by_keyword = {hit["chunk"]["id"]: hit["chunk"] for hit in keyword_hits}

    # get a cosine for the chunks that only keyword search found 
    keyword_only = [chunk_id for chunk_id in by_keyword if chunk_id not in by_vector]
    extra_cosine = chunk_index.cosine_for(strategy, query_vector, keyword_only) 

    # disagreements
    unknown = [chunk_id for chunk_id in keyword_only if chunk_id not in extra_cosine] 
    if unknown:
        raise RuntimeError(f"{unknown[0]} is in the keyword index but not in the vector index ,Rebuild with POST /knowledge/index")


    # find the numbers in the question (e.g 3307)
    wanted = identifiers(question)

    # build each final hit  
    hits = []
    for chunk_id, rrf in fused:
        if chunk_id in by_vector:
            hit = dict(by_vector[chunk_id])
        else:
            chunk = by_keyword[chunk_id]
            hit = {
                "id": chunk["doc_id"],
                "chunk_id": chunk_id,
                "title": chunk["title"],
                "text":  chunk["text"],
                "score": extra_cosine
            }
            # our 3 extra fields 
            hit["found_by"] = [name for name,found in (("vector",chunk_id in by_vector), ("keyword", chunk_id in by_keyword)) if found]
            hit["exact_match"] = bool(wanted & set(bm25.tokenize(hit["text"])) )
            hit["rrf"] = round(rrf,5)
            hits.append(hit)

    return hits 

        

    