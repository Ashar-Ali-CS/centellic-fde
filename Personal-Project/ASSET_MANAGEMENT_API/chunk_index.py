


""" 

To compare the chunk strategies

One chroma collection per chunking strategy so that can be compared side by side

Each collection rememberes a "fingerprint" of the chunks and the embedding model That built it
If either changes, the collection is rebuilt from scratch.

"""

#things to note in switch to chroma (had to insatall chromadb first)

#embed_texts() is imported not rewritten ....embeedding provider hasnt changed only the storage has 
# configuration ...-> not optimal , we are choosing something  different from chromas defualt 
# chroma returns distance , we return similairty 
# in chroma lower is better
# higher was better for ours ...(1-distance) converts    
#upsert instead of add -> add falls on an id that already exists , upsert overwrites. 


import hashlib
import chromadb

import chunking 
import knowledge_store as knowledge

from documents import DOCUMENTS
import time
from voyageai.error import RateLimitError

ALL_DOCUMENTS = DOCUMENTS 
BATCH_SIZE = 128 # Voyage's own guidence: batch documents to stay well with rate limtis 



chroma = chromadb.PersistentClient(path="./chroma_store")

def collection_name(strategy: str) -> str:
    return f"chunks_{strategy}"

def collection_for(strategy: str): 
    return chroma.get_or_create_collection(
        name= collection_name(strategy), configuration={"hnsw":{"space":"cosine"}}
                                           
        )

#makes call to voyage in groups instead of one huge request
def embed_batched(texts: list[str], input_type: str) -> tuple[list[list[float]], int]:
    """ Embed any number of texts in batches Return all vectors an total token count"""
    vectors:list[list[float]] = []
    tokens = 0 

    for start in range(0, len(texts), BATCH_SIZE):
        # Keep trying this batch until it succeeds
        batch = texts[start:start + BATCH_SIZE]
        while True:
            try:
                batch_vectors, batch_tokens = knowledge.embed_texts(batch, input_type=input_type)
                break
            except RateLimitError:
                print("\n[Rate Limit Hit] Free tier limit reached. Pausing for 60 seconds to cool down...")
                time.sleep(60)
    #    batch_vectors, batch_tokens = knowledge.embed_texts(texts[start:start + BATCH_SIZE], input_type=input_type)
        vectors.extend(batch_vectors)
        tokens += batch_tokens

    
    return vectors, tokens

  
#turns long list of texts sends chunked to voyage to store them in colleciton 
#embed_texts sends it to chroma 



#tje fingerprint chnges if text,the model or the order changes ...and stays put of nothing does 
def fingerprint(chunks: list[dict]) -> str:
    """ sqush all all chunks + model name into one short line of code 
    like a seal on parcel , so we can look if its differnt/
    - we dont have to rebuild it 
    """

    # SHA-256 is a recipe that urns every text into fixed-len code (64 char)
    digest = hashlib.sha256(knowledge.EMBED_MODEL.encode())
    for c in chunks:
        digest.update(f"{c['id']}\n{c['text']}\n".encode())

    #gives 64 char code and first 16 enough to underastand 
    return digest.hexdigest()[:16]



# NOTES:

def build(strategy: str, force: bool = False) -> dict:
    """Make sure the strategy's collection matches the current corpis,,chunker and model"""
    """Answers one q ...is the index already have still correct?"""
    #pt1
    chunks = chunking.chunk_corpus(ALL_DOCUMENTS, strategy)
    fp = fingerprint(chunks)
    col = collection_for(strategy)
    stored = col.get(limit=1, include=["metadatas"])["metadatas"]


    # pt1 
      #4 question(yes or no)
    if not force and col.count() == len(chunks) and stored and stored[0].get("fingerprint")==fp:
        return {"strategy":strategy,"chunks":len(chunks), "embedding_tokens":0, "rebuilt": False}


    # pt2 - the rebuild  - deletes old collection first (upsert adds and replaces but not removes)
    try:
        chroma.delete_collection(collection_name(strategy))
    except Exception:
        pass


    #creates new collection
    col =  collection_for(strategy)
    vectors, tokens = embed_batched([c["text"] for c in chunks], input_type="document")
    col.upsert (
        ids = [c["id"] for c in chunks],
        embeddings=vectors, 
        documents=[c["text"] for c in chunks],
        metadatas=[{"doc_id": c["doc_id"], "title": c["title"], "fingerprints":fp} for c in chunks],
    )

    return {"strategy": strategy, "chunks": len(chunks), "embedding_tokens":tokens,"rebuilt": True}



"""
CURRENT SNAPSHOT OF FLOW 

Writing

 chunking.py -> function chunk_corpus -> build -> embed_batch -> voyageai to embed -> chromadb store -> chunks stratgy stored


Reading 

Run for every query -> Question vector -> search_with_vectors(functinolity) -> Chroma -> collection chunk stratgy is queried 
-> Get back ranked hits + can derive metrics 


Adding search with vectors function to do eval harness

"""



#CURRENT - 

# NEW FUNCTION  ADD - search with vectors

#The read side 

#it takes question vectors that are already embedded, so questions are embedded once and reused across all 6 catgories 



#k is how many chunks to return 

def search_with_vectors(strategy: str, query_vectors: list[list[float]], k: int) -> list[list[dict]]:
    """
    We embed the questions once, then searches many stratgies with the same vectors. 
    """
    col = collection_for(strategy)
    if col.count() == 0:
        raise RuntimeError(f"Index for '{strategy}' is empty, build it first. ")


    #The seearch 
    result = col.query(query_embeddings=query_vectors, n_results=min(k, col.count()) )
    # what result looks like
        # - result["ids"] - a list of 2 lists, each holding 3 ids
        # - result["documents"] - a list of 2 lists, each holding 3 texts
        # - result["metadatas"] - a list of 2 lists, each holding 3 metadata dictionaires
        # - result["diatances"] - a list of 2 lists, each holding 3 distances
        # e.g. ids            ['doc-001#00', 'doc-101#01', 'doc-107#00']
        # e.g. distances      [0.375, 0.389, 0.30]
        
    return [
        # Chroma returns 4 parallel nested list 
        #per question out,per hit in.
        [
            {"id":meta["doc_id"], "chunk_id": chunk_id, "title":meta["title"], "text": text, "score":1-distance}
            for chunk_id,text,meta,distance in zip(ids,docs,metas, dists)
        ]
        for ids, docs,metas,dists in zip(result["ids"],result["documents"], result["metadatas"], result["distances"])
    ]



    # will use the eval harnes to embed all questions all at once and then pose it to the strategies 



""" 
A chunk that only keyword search found has no cosine score...our relevence gate needs one 
"""

def cosine_for(strategy: str, query_vector: list[float], chunk_ids:list[str]) -> dict[str,float]:
    if not chunk_ids:
        return {}

    stored= collection_for(strategy).get(ids=chunk_ids,include=["embeddings"])

    return {

        chunk_id: float(knowledge.cosine_similarity(query_vector,list(vector)))
        for chunk_id, vector in zip(stored["ids"], stored["embeddings"])

    }


# where it fits in hybrid.py 
    # vector search returns its top 10 with a cosine 
    # keyword search returns its top 10 
    # RRF merges them 
    # any chunk in the keyword list but NOT in the vector list is passed to "cosine_for"
    # now every hit has a cosine...so the gate works the same on all of them 
        # score >= 0.45 orrr exact match  
        




