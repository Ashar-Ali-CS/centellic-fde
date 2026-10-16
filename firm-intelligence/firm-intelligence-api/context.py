
"""
How retreived hits become the text the model reads.
Failure: lost in middle 
"""


# hits 
# not guarentee but safeguaard to help fight lost in the middle. 
def order_for_context(hits: list[dict]) -> list[dict]:
    """ ORDERING STRONGEST/RELEVENT EVIDENCE IN THE EDGES - 
    Orderd like-Best hit first,second best last, weakest in middle """
    ranked = sorted(hits,key=lambda h: h["score"],reverse=True)
    front = hits[0::2]
    back = hits[1::2]
    return  front + back[::-1]




def build_context(hits: list[dict]) -> str:
    """The exact text block the model sees, one labelled section per hit."""
    return "\n\n".join(f"[{h['id']}] {h['title']}\n{h['text']}" for h in order_for_context(hits))