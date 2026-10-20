
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
    return SearchClient(endpoint=_endpoint(), index_name=settings.AZURE_SEARCH_INDEX, credential= _credential())


@lru_cache(maxsize=None)
def index_client() -> SearchIndexClient:
    return SearchIndexClient(endpoint=_endpoint(), credential=_credential())

#like one in hybrid.py (if we get rid of hybrid.py and use this. )
def _identifiers(text: str) -> set[str]:
    """Tokens containing a digit (e.g 3307),same as in hybrid.py""" 
    return {token for token in bm25.tokenize(text) if any(ch.isdigit() for ch in token)}


def count() -> int:
    """ Number of chunks in Azure index, 0 if it does not exist 
        - Needs only the query permission.
    """
    try:
        return search_client().search(search_text = "*", include_total_count=True, top=0).get_count()
    except ResourceNotFoundError:
        return 0 


#MAIN EVENTS

# search with vector
# get every chunk from its Voyage vector 
# makes new documents searchable 
# drop and recreate index 


def search_with_vector(question:str, query_vector: list[float], top_k: int = 3, semantic: bool=True) -> list[dict]:
   
    # 1 - clean the questions
        # what is "LP-3307"? becomes 
        #what is lp 3307 

    search_text = " ".join(bm25.tokenize(question)) or "*"


    # 2 - build one query that will do 2 searches
        #keyword half and vector half 
    

    options = {
        "search_text":search_text,
        "vector_queries": [VectorizedQuery(vector=query_vector, k_nearest_neighbors=CANDIDATES, fields="embedding")],
        "select": ["chunk_id", "doc_id", "title", "text"],
        "top": max(top_k, CANDIDATES),
    }

    # 3 - switch on the semantic reranker

    if semantic:
        options["query_type"] = "semantic"
        options["semantic_configuration_name"] = settings.SEMANTIC_CONFIG

    # 4 - run it , trim it(top k), if needed handle any missing index
    #handling if index not built, runs search and keeps top_k , ** unpacks options  dicternioary into accessable.
    try:
        results = list(search_client().search(**options))[:top_k]
    except ResourceNotFoundError as error:
        raise RuntimeError(NOT_BUILT) from error

    if not results:
        raise RuntimeError(NOT_BUILT)


    # 5 - turn each result into a hit 
        # two scores : reranks score(0-4), and the fused rank score from the merge. 

    wanted = _identifiers(question) if settings.EXACT_MATCH_RULE else set()
    hits = []

    for result in results:
        rerank = result.get("@search.reranker_score")
        fused = result["@search.score"]
        text_tokens = set(bm25.tokenize(result["text"]))

        hits.append({
            "id": result["doc_id"],
            "chunk_id": result["chunk_id"],
            "title": result["title"],
            "text": result["text"],
            "score": rerank if rerank is not None else fused, 
            "rerank_score": rerank, 
            "rrf": round(fused, 5),
            "exact_match": bool(wanted & text_tokens),
        })
    return hits 



#def _local_chunks(strategy:str) -> list[dict]:
    """
    Every chunk with its Voyage vector
    Reusing the vectors costs no embedding tokens (also means Azure has the exact same chunks and vectors as local search)
    """

 #   chunk_index.build(strategy) # free when up to date 

    # stored is a dict of parrallel lists 
        # stored["ids"], stored["embeddings"]....
   # stored = chunk_index.collection_for(strategy).get(include=["embeddings","documents","metadatas"])

    #walk all 4 lists together
   # return [
   #     {
   #        "chunk_key": azure_index.key_for(chunk_id),
   #         "chunk_id": chunk_id,
   #         "doc_id": meta["doc_id"],
   #         "title": meta["title"],
   #         "text": text,
   #         "embedding": [float(number) for number in vector],
   #     }
   #     for chunk_id, vector, text, meta in zip(stored["ids"],stored["embeddings"],stored["documents"],stored["metadatas"])
   # ]
def _local_chunks(strategy: str) -> list[dict]:
    chunk_index.build(strategy) 
    stored = chunk_index.collection_for(strategy).get(include=["embeddings", "documents", "metadatas"])

    docs = []
    for chunk_id, vector, text, meta in zip(stored["ids"], stored["embeddings"], stored["documents"], stored["metadatas"]):
        
        # Convert numpy array to list if needed, and handle nested lists safely
        if vector is not None:
            if hasattr(vector, "tolist"):
                vector = vector.tolist()
            if len(vector) > 0 and isinstance(vector[0], list):
                vector = [num for sublist in vector for num in sublist]
            flat_vector = [float(num) for num in vector]
        else:
            flat_vector = []

        docs.append({
            "chunk_key": azure_index.key_for(chunk_id),
            "chunk_id": str(chunk_id),
            "doc_id": str(meta.get("doc_id", "")),
            "title": str(meta.get("title", "")),
            "text": str(text),
            "embedding": flat_vector,
        })
    return docs

def _wait_until_counted(expected: int, seconds:int = 30) -> None: 
    """
    New documents become searchable a moment after upload, so we wait for the count to catch up . 
    """
    deadline = time.time() + seconds 
    while time.time(): 
        if count() >= expected:
            return
        time.sleep(1)
    raise RuntimeError(f"Uploaded {expected} chunks, but the index reports {count()} after {seconds} seconds.")




def build_index(strategy:str) -> int:
    """
    Drop and recreate the Azure index ... then load every chunk...return chunk count.
    """

    docs = _local_chunks(strategy)
    keys = [doc["chunk_key"] for doc in docs]
    if len(set(keys)) != len(keys):
         # the ids of doc-1#01 and doc1_01   would both become doc-1_01 
        raise RuntimeError("Two chunk ids turn into the same Azure key, so chunks would overwrite each other")
    
    #check the vector sizes
    bad = [doc for doc in docs if len(doc["embedding"]) != azure_index.DIMENSIONS]
    if bad: 
        raise RuntimeError(f"{bad[0]['chunk_id']} has {len(bad[0]['embedding'])} numbers per vector , but index expects {azure_index.DIMENSIONS}. Did embeddinng model change?")
    

    #can now replace index. 
    name = settings.AZURE_SEARCH_INDEX
    try:
        index_client().delete_index(name)
    except ResourceNotFoundError:
        pass
    index_client().create_index(azure_index.index_definition(name))

                               

    #100 chunks , looping 
    for start in range(0, len(docs), BATCH):
        results = search_client().upload_documents(documents=docs[start:start + BATCH])
        failed = [result for result in results if not result.succeeded]
        if failed: 
            raise RuntimeError(f"Azure rejected {len(failed)} chunks. First: {failed[0].key}: {failed[0].error_message}")


    # wait, then report 
    _wait_until_counted(len(docs))
    return len(docs)



