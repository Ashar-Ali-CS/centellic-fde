

""" 

Chunking strategies
Every strategy takes a document and returns a list of chunks.


A chunk is a dict:
     - id       <doc_id>#<two-digit-number>, kept stable for the same output 
     - doc_id    the parent document , use for citations (which doc the chunk is part of )
     - title     the parent documents title
     - text      exactly what gets embeded and what the model will read 

"""

import re



#helper functions to help chunking  strategie's later 

def _chunk(doc: dict, number: int, text: str ) -> dict:

    """Builds chunk digits from doc 
     # 2->02
     # with padding - [doc-105#01], [doc-105#02], [doc-105#03]
     #helps sort later 
     """
    
    return { "id": f"{doc["id"]}#{number:02d}", "doc_id": doc["id"] , "title": doc["title"], "text": text }


def split_sentances(text: str) -> list[str]:
    """ Takes text and breaks into Sentences
    Sentances,with each '## Heading' line kept as a unit of its own
    """
    units = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue 

        if line.startswith('## '):
            units.append(line) 
        else:
            #cut normal text into sentances to have ending (  . / ! / ? ) (checks if white space after . to not decimal like 5.2 )
      #      units.extend(s for s in re.split(r"?<=[.!?]\s+", line) if s ) 
            units.extend(s for s in re.split(r"(?<=[.!?])\s+", line) if s)
    return units 



def pack( units: list[str], max_words: int) -> list[str]:
    """ Join whole units until adding the next one would pass max words - 
    when we exced whats set as max words - this function pushes it into next chunk as needed. """


    #groups holds finished chunks, current is the chunk being built and count is its word total. 
    groups, current , count = [], [], 0 

    for unit in units:
        n = len(unit.split())

        # if it exceeds the max_words. 
        if current and count + n > max_words:
            groups.append(" ".join(current))
            current, count = [], 0 

        #otherwise contiunue 
        current.append(unit)
        count += n

    if current: 
        groups.append(" ".join(current))

    return groups




#============================CHUNKING STRATEGIES====================================================================



#  1 - Whole document (baseline)

#can use if small documents 
def whole_document(doc: dict) -> list[dict]:
    """ Baseline ....what project has done until now """
    return [_chunk(doc,0,doc["body"].strip())]






# 2 - fixed_words (usally 100 ) and 
# 3 - fixed_words _with overlap?-this function is basicly same as but with 25% overlap instead of 0 

# can use if structure of data relies on word count reliably (100 words sentances)
# or if no structure whats so ever (calls/meeting transcripts,pages/call logs) 
def fixed_words(doc: dict, size: int=100, overlap: int=0 ) -> list[dict]:
    """Every "size"  words, regardless of sentances or section. Cheap and blind"""

    #But cant have overlap at least 0 and smaller then size of chunk (must be fraction)
    if not 0 <= overlap <size:
        raise ValueError("overlap must be at least 0 and smaller than size")

    words = doc["body"].split()
    step = size - overlap 
    chunks = []

    #range(0,385,75)
    for number, start in enumerate(range(0,len(words),step)):
        chunks.append(_chunk(doc, number, " ".join(words[start:start+size])))

        #stop when window reaches end of doc 
        if start + size >= len(words):
            break 

    return chunks


# 4- Sentance 
# sentencepacked
def sentence_packed(doc: dict, max_words: int = 100) -> list[dict]:
    """Whole sentences only, packed up to max_words. Never cuts a sentence in half."""
    return [_chunk(doc, n, text) for n, text in enumerate(pack(split_sentances(doc["body"]), max_words))]


# 5 - Sections plain 
# 6 - Sections contextual 
#  One function reusable for both ( defualt contextual )

def by_sections(doc:dict, max_words:int=150 , contextual:bool = True) ->list[dict]:
    """ 
        One chunk per '## ' section... long sentances are packed by section
        contextual=True prefixes each chunk with "Document title > section heading", 
        ...so a chunk that never names its subject still carries it into the  embbedding.
    """

    chunks, number = [], 0 
    parts = re.split(r"(?m)^## ", doc['body']) if "## " in doc['body'] else [doc['body']]

    for part in parts:
        #heading, _, text = part.partition("\n" if "## " in doc["body"] else ("","",part))
        #heading, text = heading.strip(), text.strip()
        # Check if sectioning occurred
        if "## " in doc["body"]:
            heading, _, text = part.partition("\n")
        else:
            heading, text = "", part
        if not text:
            continue

        for piece in pack(split_sentances(text),max_words):
            if contextual:
                prefix = f"{doc['title']} > {heading}\n" if heading else f"{doc['title']}\n"
                piece = prefix + piece

            chunks.append(_chunk(doc,number,piece))
            number += 1 


    return chunks 




STRATEGIES = {
    "whole_document":whole_document,
    "fixed_100": lambda d: fixed_words(d,size=100, overlap=0),
    "fixed_overlap_25": lambda d:fixed_words(d,size=100, overlap=25),
    "sentences_100": lambda d: sentence_packed(d, max_words=100),
    "sections_plain": lambda d: by_sections(d, max_words=150,contextual=False),
    "sections_contextual": lambda d: by_sections(d, max_words=150,contextual=True),
}


def chunk_corpus(docs: list[dict], strategy:str) -> list[dict]:
    return [ chunk for doc in docs for chunk in STRATEGIES[strategy](doc)]



#import chunking, corpus,documents

#from documents import DOCUMENTS 
# from corpus import CORPUS_DOCUMENTS
#from chunking import STRATEGIES, chunk_corpus


#ALL_DOCS = DOCUMENTS + CORPUS_DOCUMENTS

#for s in STRATEGIES: 
#    num_chunks= len(chunk_corpus(ALL_DOCS, s))
#    print(f"FOR STRATEGY {s}  THE NUMBER OF CHUNKS = {num_chunks}")



