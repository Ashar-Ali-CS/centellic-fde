

"""Checks on generated answers. Pure Functions: no network calls,no model ,no FastAPI


Failure 1 - ungrounded hallucination: sentances that carry no citation at all 

Failure 2 - Citation drift - citations that point at the wrong source or no source." 


"""



import re

REFUSAL_SENTANCE = "The provided documents do not answer that question."



# the findall will return doc-001,rather than [doc-001]  
CITATION = re.compile(r"\[(doc-\d{3})\]")


#Pure functions - 

#normalise function - lower-case and squish every run of spaces,tabs/newlines into one space.
#we need this as models sometimes wrap lines ...so without normalise a refusal split across two lines would not match 
def normalise(text:str) -> str:
    if text is None:
        return ""
    return re.sub(r"\s+", " ", text).strip().lower() 




#is_refusal function - treats None as a refusal too 
#we are standardising the refusal.
# /knowledge/ask returns answer None when it refuses before calling the model ,and the check should agree with the endpoint. 
def is_refusal(answer:str | None) -> bool:
    return answer is None or normalise(REFUSAL_SENTANCE) in normalise(answer) 





#citation cheker
#citation without citation is a sentance that cant be tied to citation so might be hallucaination. 
def split_sentances(text: str) -> list[str]:  
    """SPLLT AN ANSWER INTO SENTANCES, KEEPTING A TRAILING CITATION WITH ITS SENTANCE.

    Models can write both 'Revenue rose [doc-001]. ' and 'Revenue rose.[doc-001]' 
    The second form would otherwise leave [doc-001] as a sentance of its own.
    """
    pieces = []

    for line in text.splitlines():
        line = line.strip(" -*\t")
        if line: 
            pieces.extend(p for p in re.split(r"(?<=[.!?])\s+",line) if p)


    #refactors text ,dont want citation after sentancethat gets taken into another sentance. 
    sentances: list[str] = []
    for piece in pieces: 
        if sentances and CITATION.sub("", piece).strip(" .") == "":
            sentances[-1] = f"{sentances[-1]} {piece}"
        else: 
            sentances.append(piece)
    return sentances 



#citations_in 
def citations_in(text:str) -> list[str]:
    return CITATION.findall(text)

#check_citations 
def check_citations(answer:str | None, source_ids: list[str]) -> dict:
    """Cheap structural checks on answers. Catches uncited claims and citations to soures we never gave
    """

    if is_refusal(answer):
         return {"refusal": True, "cited": [], "invalid": [], "uncited_sentances": [], "passed": True}

    sentances = split_sentances(answer) 
    cited = sorted(set(citations_in(answer) ))
    invalid = [doc_id for doc_id in cited if doc_id not in source_ids]
    
    #very shourt sentances are claims not worth policing with citataions. 
    uncited = [ s for s in sentances if not CITATION.search(s) and len(s.split())>=3]

    return{
        "refusal": False,
        "cited": cited,
        "invalid": invalid,
        "uncited_sentances": uncited,
        "passed": not invalid and not uncited, 
    }



