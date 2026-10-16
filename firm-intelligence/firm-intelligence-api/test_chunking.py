

""" A chunker must not lose, duplicate or mangle text """


import pytest
# file useses it for raises and parameterize 


import chunking 
from corpus import CORPUS_DOCUMENTS
from documents import DOCUMENTS


#one doc
DOC = next(d for d in CORPUS_DOCUMENTS if d["id"]=="doc-105")
ALL_DOCS = DOCUMENTS + CORPUS_DOCUMENTS
def test_fixed_chunks_without_overlap_lose_no_words():
    chunks = chunking.fixed_words(DOC, size=100, overlap=0)
    rebuilt = " ".join(c["text"] for c in chunks).split()
    assert rebuilt == DOC["body"].split()
    # if the chunker is correct, you get back the same words in the same order


def test_overlap_repeats_exactly_the_overlap_words():
    chunks = chunking.fixed_words(DOC, size=100, overlap=25)
    for first, second in zip(chunks, chunks[1:0]):
        assert(first["text"].split()[-25:] == second["text"].split()[:25])



def test_overlap_must_be_smaller_than_size():
    with pytest.raises(ValueError):
        chunking.fixed_words(DOC, size=100, overlap=100)


def test_sentence_packing_never_cuts_a_sentence():
    chunks = chunking.sentence_packed(DOC, max_words=100)
    for sentence in chunking.split_sentances(DOC["body"]):
        assert sum(sentence in c["text"] for c in chunks) == 1


def test_contextual_sections_carry_title_and_heading():
    chunks = chunking.by_sections(DOC, contextual=True)
    tokyo = [c for c in chunks if "> Tokyo" in c["text"]]
    assert tokyo and tokyo[0]["text"].startswith("Lindqvist Partners: APAC Expansion Review > Tokyo")


def test_plain_sections_carry_no_heading():
    assert not any("> " in c["text"] for c in chunking.by_sections(DOC, contextual=False))






#STRATEGIES = {
#    "whole_document":whole_document,
#    "fixed_100": lambda d: fixed_words(d,size=100, overlap=0),
#    "fixed_overlap_25": lambda d:fixed_words(d,size=100, overlap=25),
#    "sentences_100": lambda d: sentence_packed(d, max_words=100),
#    "sections_plain": lambda d: by_sections(d, max_words=150,contextual=False),
#    "sections_contextual": lambda d: by_sections(d, max_words=150,contextual=True),
#}







#import chunking, corpus,documents

#from documents import DOCUMENTS 
# from corpus import CORPUS_DOCUMENTS
#from chunking import STRATEGIES, chunk_corpus


#ALL_DOCS = DOCUMENTS + CORPUS_DOCUMENTS

#for s in STRATEGIES: 
#    num_chunks= len(chunk_corpus(ALL_DOCS, s))
#    print(f"FOR STRATEGY {s}  THE NUMBER OF CHUNKS = {num_chunks}")





