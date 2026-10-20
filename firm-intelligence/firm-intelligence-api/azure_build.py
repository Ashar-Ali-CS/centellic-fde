
"""
THE ENRY POINT 
Create the Azure index and load every chunk into it 
We run it from project root: python -m azure_build 
"""

import azure_store #build index
import knowledge_store  # chunk strategy 
import settings # azure settings and endpoint. 

def main() -> None:
    loaded = azure_store.build_index(knowledge_store.CHUNK_STRATEGY)
    print(f"Loaded {loaded} chunks into '{settings.AZURE_SEARCH_INDEX}'  at  {settings.AZURE_SEARCH_ENDPOINT} ")


if __name__ == "__main__":
    main()



