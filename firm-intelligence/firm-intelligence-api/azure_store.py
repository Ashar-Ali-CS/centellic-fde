
"""
Azure AI Search backend ....this is going to do the same job as knowledge_store (count, build_index, search).

On search call does 3 things: 
1. Keyword search(BM25) and vector search run together, and Azure fuses them with RRF.
2. the semantic reranker rereads the top results beside the question and scores each 0 
3. the hits come back first , carrying that score for the relevence gate(gate.py)

#not an LLM but model based on transformer/encoder to rank 

"""


import time
from functools import lru_cache

from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential 
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.models import VectorizedQuery

import azure_index
import bm25
import chunk_index
import settings


# semantic ranker only ever reads top 50 results, so we'll ask for that many and trim to top_k afterwards
CANDIDATES = 50 


#chunks per upload request 
BATCH = 100 


#error message
NOT_BUILT = "The Azure index is empty or missing. Build it with python -m azure_build"



# pt2 - signing in and the two clients 


#work out once and reuse answer(creates defualt credientials and returns )
@lru_cache(maxsize=None)
def _credential() -> DefaultAzureCredential:
    """Signs in as you after 'az login' , or  as the managed identity once deployed"""
    return DefaultAzureCredential()

def _endpoint() -> str:
    if not settings.AZURE_SEARCH_ENDPOINT:
        raise RuntimeError("AZURE_SEARCH_ENDPOINT is not set." \
        "Example: export= AZURE_SEARCH_ENDPOINT = https://<your-service>.search.windows.net")
    
    return settings.AZURE_SEARCH_ENDPOINT


#two handled seperatly

@lru_cache(maxsize=None)
def search_client() -> SearchClient:
    return SearchClient(endpoint=_endpoint(), index_name=settings.AZURE_SEARCH_INDEX, credentials= _credential())


@lru_cache(maxsize=None)
def index_client() -> SearchIndexClient:
    return SearchClient(endpoint=_endpoint(), credentials= _credential())

#like one in hybrid.py (if we get rid of hybrid.py and use this. )
def identifiers(text: str) -> set[str]:
    """Tokens containing a digit (e.g 3307),same as in hybrid.py""" 
    return {token for token in bm25.tokenize(text) if any(ch.isdigit() for ch in token)}


def count() -> int:
    """ Number of chunks in Azure index, 0 if it does not exist 
        - Needs only the query permission.
    """
    try:
        return search_client().search(search_texts = "*", include_total_count=True, top=0).get_count()
    except ResourceNotFoundError:
        return 0 


#MAIN EVENT 

def search_with_vector(question:str, query_vector: list[float], top_k: int = 3, semantic: bool=True) -> list[dict]:
   
    # 1 - clean the questions
        # what is "LP-3307"? becomes 
        #what is lp 3307 



    # 2 - build one query that will do 2 searches
        #keyword half and vector half 
    


    # 3 - switch on the semantic reranker


 
    # 4 - run it , trim it(top k), if needed handle any missing index



    # 5 - turn each result into a hit 
        # two scores : reranks score(0-4), and the fused rank score from the merge. 

    
    pass 


