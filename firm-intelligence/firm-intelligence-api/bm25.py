

"""
BM25 keyword search....build by hand first so we can see every  term in the score.
Dont need to do this (just how it works )


No network, no model calls
It will index the same chunks the vector index holds....so our 2 retrivers can be fused chunk for chunk 

"""

# fusion is next 



import math 
import re 
from collections import Counter

K1 = 1.5 # how quickly repeating a word stops adding score
B = 0.75 # how strongly long chunks are marked down 

# tokenize - turns text to lowercase words and number 

    #splits at -
    # "LP-3307" becomes ["lp","3307"]
    # "what is lp 3307 about? "  ->   ["what","is","lp","3307","about"]
    # Walkthrough 
        # what, is and about appear in many chunks so they add very little
        # 3307 appears in one chunk, the tokyo one so it will carry highest rarity 
         # most of the chunks with the winning score comes from the rare tokens it shares with the question


    # fusion


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())



# BM25 Class 
    #idf 
    #score 
    #search 


#initilise


class BM25Index:
    def __init__(self, chunks: list[dict]):
        # Guardrail - cant build key word without chunks 
        if not chunks: 
            raise ValueError("cannot build a keyword index from zero chunks")
        self.chunks = chunks
        self.term_counts = [Counter(tokenize(c["text"])) for c in chunks]
        self.lengths = [sum(counts.values()) for counts in self.term_counts]
       # self.lengths = [sum(counts()) for counts in self.term_counts ]
        self.avg_length = sum(self.lengths) / len(chunks)

        self.doc_freq = Counter()
        for counts in self.term_counts:
            self.doc_freq.update(counts.keys())
        #count everything upfront(chunks,len,document frequency etc )


    def idf(self, term: str) -> float:
        """How rare an item is. Rare term scores high, word in every chunk scores near zero."""
        n = len(self.chunks)
        df = self.doc_freq.get(term,0)

        #logarithmic? 1 and 2 more differnt with on way higher than 56 and57 (which are closer)
        return math.log(1 + (n - df + 0.5) / (df + 0.5))


    def score(self, query_terms: list[str], position:int) -> float:
        """BM25 score of one chunk(by its position in the list)...for a list of query items"""
        counts = self.term_counts[position]
        length_norm = 1 - B + B * self.lengths[position] / self.avg_length

        total = 0.0 

        for term in set(query_terms):
            tf = counts.get(term, 0)
            if tf:
                total += self.idf(term) * tf * (K1 + 1) / (tf + K1 * length_norm)
                total += self.idf(term) * tf * (tf + K1 * length_norm)
        return total

    def search(self, query:str, k: int = 10) -> list[dict]:
        """The k best chunks for a query ....best first. Chunks that share no word with it are left out """

        terms = tokenize(query)
        scored = []

        for position, chunk in enumerate(self.chunks):
            bm25 = self.score(terms,position)
            if bm25 > 0:
                scored.append({"chunk":chunk,"bm25": bm25})
        scored.sort(key=lambda hit: hit["bm25"], reverse=True)
        return scored[:k]

    


# why we need both types of search

# Keyword search (BM25)
    # Good at.... Exact codes, names and numbers (LP-3307)
    # Bad at... Synonyms and paraphrase

# Vector search
    # Good at... Meaning ("income" matching "revenue")
    # Bad at... codes that carry no meaning


    #TOMMAROW
    #reciprocal rank fusion to merge them using order only 

    # 4/5 functions 

    #hybrid vs vector search. 

 

    #FRIDAY 

    # NEED TO IMPLMEENT AI SEARCH IN PUBLIC 

    # MOCK INTERVIEW (TOPICAL )

    # PROJECT WORK -

    #  Add final features AI search

     #LLM as a judge 


    #LangChain

    #Agentic patters 

    #MCP and guardrails 

    #Deploying,versioning and drift. 


    

