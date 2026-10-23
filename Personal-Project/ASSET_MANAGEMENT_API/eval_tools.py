
"""
Small , pure helper functions  for scoring. No network and no model.

"""


import re 
   
from grounding import is_refusal, normalise # one definition for refusal 


def contains_evidence(chunk_text:str, evidence:str) -> bool:
    """ True if the chunk holds the whole evidence span. Line breaks never break a match """

    return normalise(evidence) in normalise(chunk_text)


# alternetive matches 
def _alternative_matches(answer:str, alternative:str) -> bool:
    """ Uses Re """

    prefix = alternative.endswith("*")
    core = re.escape(alternative.rstrip("*").lower())
    ending = "" if prefix else r"(?![a-z0-9])"
    return re.search(rf"(?<![a-z0-9]){core}{ending}", answer.lower()) is not None


# keywords_present
# what the keywords list looks like 
def keywords_present(answer:str | None, keywords: list[str]) -> bool:
    """ True only for a non-refusal answer that containes every keyword group """
    #refusal can never be correct answer 
    if is_refusal(answer):
        return False

    return all(
        any(_alternative_matches(answer,alt) for alt in group.split("|")) for group in keywords
    )

    
