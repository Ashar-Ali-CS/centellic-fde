


#embedding provider has not changed ...only where vectors stored 

import chromadb

import voyageai

from documents import DOCUMENTS



EMBED_MODEL = "voyage-3-lite"

voyage = voyageai.Client(
    api_key=os.environ["VOYAGE_API_KEY"],
    max_retries=3,
    timeout = 3
)



chroma = chromadb.PersistentClient(path="./chroma_store")


#configuration line not optional , defualt is not cosine similarity 

collection = chroma.get_or_create_collection(
    name="firm_documents",
    # HNSW ( hierarcihcal navigable small world - graph based index used in vector databases-
    #-to perform fast and approportie neerest neibhour search in high dimensional data 
    configuration={"hnsw": {"space": "cosine" }},
)


def count() -> int:
    return collection.count()

def build_index() -> int:
    """ Embed every document and hand the vectors to Chroma db """
    texts = [doc["body"] for doc in DOCUMENTS]
    vectors, tokens = embed_texts(texts,input_type="document")

    #if it already exists,upsert overwrites it(add would throw error) or if it doesnt it will create.
    collection.upsert(
        ids =[doc["id"] for doc in DOCUMENTS],
        embeddings=vectors, 
        documents=texts,
        metadatas=[{"title":doc["title"], "type": doc["type"]} for doc in DOCUMENTS]
    )

    return tokens 

# our function
def search(question: str, top_k:int=3) -> list[dict]:
    """ Embed the question and let Chroma do the storing """

    # _ underline to store a variable not used
    query_vectors, _  = embed_texts([question], input_type="query")

    result = collection.query(query_embeddings=query_vectors , n_results=top_k ) 

    return [
        {
            "id":doc_id,
            "title":metadata["title"],
            "text": text,

            #Chroma will give us back distance ...lower is closer
            # does ( 1-distance) in order to flip from return distance, to simlairty 
            "score": 1- distance,
        }
        for doc_id, text,metadata,distance in zip(
            result["ids"][0],
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
        )
    ]

    




def embed_texts(texts: list[str] ,  input_type: str)-> tuple[list[list[float]]]:
    #embed a batch
    # input type tells voyage wheter these are docs or query (done differently by voyage) 
    result = voyage.embed(texts=texts,model=EMBED_MODEL, input_type=input_type)
  
    #returns the vectors and token count (can see cost)
    return result.embeddings, result.total_tokens





#things to note in switch to chroma (had to insatall chromadb first)




# configuration ...-> not optimal , we are choosing something  different from chromas defualt 
# chroma returns distance , we return similairty 
# in chroma lower is better
# higher was better for ours ...(1-distance) converts    

#upsert instead of add -> add falls on an id that already exists , upsert overwrites. 


#refacotring steps tommarow ,rapid UI prototyping (spec driven AI ,interacting with chroma db),
#context engineering theory




