

"""

What a chunk looks like inside Azure AI Search- one place defines our index. 

Fields 
    - chunk_key
    - chunk_id
    - doc_id 
    - title 
    - text 
    - embedding 

"""


from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    HnswParameters,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SearchableField,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    VectorSearch,
    VectorSearchProfile,
)

