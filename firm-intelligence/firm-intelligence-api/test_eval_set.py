


import re

from corpus import CORPUS_DOCUMENTS
from documents import DOCUMENTS
from eval_set import EVAL_SET, answerable 
from eval_tools import contains_evidence, keywords_present, normalise


ALL_DOCS = {d["id"]: d for d in DOCUMENTS + CORPUS_DOCUMENTS}


def section_containing(body: str, evidence: str) -> tuple[str,str]:
    """Return (heading,section text) for the section holding the evidence"""
    for part in re.split(r"(?m)^## ", body):
        heading, _, text = part.partition("\n")
        if contains_evidence(text,evidence):
            return heading.strip(), text
    raise AssertionError(f"evidence not found in any section: {evidence}")

# test ids are unique 
def test_id_unique():
    """ Loops through all tests in EVAL_set , fails if duplicate id detectd"""
    seen_ids = []
    duplicate_id_detected =[]
    for test in answerable():
        #checks if doc id is already 
        if test["id"] in seen_ids:
            duplicate_id_detected(test["id"])
        seen_ids.append(test["id"])
    #If duplicates detected ,it means test ids are NOT unique 
    assert duplicate_id_detected == []



# test every evidence span is  in its own documents 

def test_evidence_span_in_own_doc():

    for item in answerable():
        # Checks for doc id in eval_set answerables(with doc id)
        doc_id = item["doc_id"]
        assert doc_id in ALL_DOCS, f"Missing doc_id '{doc_id}' for question ID '{item['id']}'"

        #gets doc with that id  + evidence from test eval assoacited item
        doc = ALL_DOCS[doc_id]
        evidence = item["evidence"]

        # Check if the evidence string is present in the document body
        assert contains_evidence(doc["body"], evidence), (
            f"Question '{item['id']}': Evidence '{evidence}' not found in document '{doc_id}'"
        )
    


#test every evidence span appears exactly once in whole corpus 
#def test_evidence_space_appears_once_in_whole_corpus():
#    failures=[]
#    for item in answerable:
#        evidence = item["evidence"]
#        #hits = item_id for doc_id, doc in ALL_DOCS.items() if con

        #pass





#test keyword matching in whole word and refusal aware 


# test ids are unique
def test_ids_are_unique():
    ids = [q["id"] for q in EVAL_SET]
    assert len(ids) == len(set(ids))

# test every evidence span is in its documents
def test_every_evidence_span_is_in_its_document():
    for q in answerable():
        assert contains_evidence(ALL_DOCS[q["doc_id"]]["body"], q["evidence"]), q["id"]

# test every evidence span appears exactly once in the whole corpus
def test_every_evidence_span_appears_exactly_once_in_the_whole_corpus():
    for q in answerable():
        total = sum(normalise(d["body"]).count(normalise(q["evidence"])) for d in ALL_DOCS.values())
        assert total == 1, f"{q['id']} evidence appears {total} times"

# test keyword matching in whole word and refusal aware
def test_keyword_matching_is_whole_word_and_refusal_aware():
    assert keywords_present("There are no outstanding matters [doc-104].", ["no|none"])
    assert not keywords_present("The provided documents do not answer that question.", ["no|none"])
    assert not keywords_present("Revenue was 120 million.", ["12"])
    assert keywords_present("They are excluded [doc-107].", ["exclud*"])
    assert keywords_present("Offices in Lagos and Nairobi.", ["Lagos", "Nairobi"])
    assert not keywords_present("An office in Lagos.", ["Lagos", "Nairobi"])