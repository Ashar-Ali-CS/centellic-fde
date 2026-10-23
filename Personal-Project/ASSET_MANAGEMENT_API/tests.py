

# Tests with the LLM and embedding calls mocked.
#  Cover at least the summary, the refusal rule and the agent loop, including the iteration limit.




import anthropic
from fastapi.testclient import TestClient


import knowledge_store as knowledge
import agent_settings as agent

from main import app

import httpx
import llm



client = TestClient(app)




# FAKE SUMMARY OF CLIENT PORTFOLIO 1  ( this isnt a client or real - its just something for fake LLM to test)

FAKE_SUMMARY = {
    "id": 1, "name": "Harding & Voss", "summary": "A fixture company",
    "input_tokens": 120, "output_tokens": 95, "stop_reason": "end_turn"
    }





"""THE BREIF SAYS - - Tests with the LLM and embedding calls mocked. Cover at least the summary, the refusal rule
  and the agent loop, including the iteration limit.
  

  Right now:
  > Test LLM summary(without mode) implemented
  > Test refusal rule - one implmeneted, working on vector search tests(with mocked embedding calls)
  > Working on Agent testing 
  """

# ----------- TESTS FOR LLM(monkeypatch stops model calls) --------------



#Testing summarise fund_factsheets 

def test_summary_returns_text_and_summary(monkeypatch):
    monkeypatch.setattr(llm, "summarise_fund_factsheet", lambda fund: FAKE_SUMMARY)
    response = client.post("/llm/summary/1")
    #assert what it should do 
    assert response.status_code ==200
    assert response.json()["input_tokens"] == 120


def test_provider_timeout_becomes_504(monkeypatch):
    def boom(firm):
        raise anthropic.APITimeoutError(request=None)
    monkeypatch.setattr(llm, "summarise_fund_factsheet",boom)
    response = client.post("/llm/summary/1")
    assert response.status_code == 504







# ----------- TESTS FOR VECTOR SEARCH EMBEDDINGS (no real embedding calls) --------------






#TESTING REFUSAL RULE 


def test_short_question_is_rejected_before_any_work():
    assert client.post("/knowledge/ask", json={"question": "hi"}).status_code == 422





# ----------- TESTS FOR AGENT AND MAX ITERATIONS --------------


#Helpers 
class FakeToolUseBlock: 
    def __init__(self, input_):
        self.type = "tool_use"
        self.id = "toolu_01"
        self.name = "search_knowledge_base"
        self.input = input_
class FakeUsage: 
    def __init__(self, i , o ):
        self.input_tokens, self.output_tokens = i,o
class FakeResponse:
    def __init__(self,content,stop_reason, usage):
        self.content, self.stop_reason, self.usage = content, stop_reason, usage



#TESTING MAX ITERATIONS

#**kwargs - accepts anything (no matter how many arguements)
# a test arguement 
def test_agent_stops_at_max_iterations_instead_of_looping_forever(monkeypatch):
    def fake_create(**kwargs):
        return FakeResponse (
            [FakeToolUseBlock({"query": "anything"})],"tool_use", FakeUsage(100,15)
    )

    monkeypatch.setattr(agent.client.messages, "create",fake_create)
    monkeypatch.setattr(
        agent.knowledge, "search",
        lambda q ,top_k=3: [{"id":"doc-001","title": "title","text":"x","score":0.5}]
    )

    response = client.post("/agent/ask", params={"question": "never resolves"})
    body = response.json()

    #assert = completed 

    assert response.status_code ==200  

    #assert - stop reoson

    assert body["stop_reason"] == "max_iterations"

    #assert- tool_calls made

    assert body["tool_calls_made"] == agent.MAX_ITERATIONS








# -------------- TESTS FOR GROUNDING ----------------





import grounding 



#This is random fake sources , this is just to test my grounding.check_citations() works 
SOURCES = {
    "doc-101": "Harding and Voss closed the  year with revenue of $1.24 billion, up 4.1%.",
    "doc-107": "fixed=share partners are excluded from the equity partner count.",
}


# Failure 1 - ungrounded claims 

# test that refusal needs nocitations
def test_refusal_needs_no_citations():
    report = grounding.check_citations(grounding.REFUSAL_SENTANCE, ["doc-101"])
    assert report["refusal"] is True and report["passed"] is True   



#test fully cited answer passes
def test_fully_cited_answer_passes():
    answer = "revenue grew by 4.1 percent.[doc-101]"
    report = grounding.check_citations(answer, ["doc-101"] )
    assert report["refusal"] is False and report["passed"] is True
    assert len(report["cited"]) ==1 



#test uncited sentance is flagged 
def test_uncited_sentance_is_flagged():
    answer = "Revenue grew by 4.1 percent.[doc-101]. The firm is one of largest in europe. " 
    report = grounding.check_citations(answer, ["doc-101"] )
    assert report["uncited_sentances"] is not None 
    assert report["uncited_sentances"] == ["The firm is one of largest in europe."]
    assert report["passed"] is False


#test citation after full stop still counts   
def test_citatation_after_full_stop_counts():
    answer = "Harding & Voss closed the year with revenue of 2.1 billion.[doc-101]"
    report = grounding.check_citations(answer, ["doc-101"] )
    assert  report["passed"] is True
    assert report["uncited_sentances"] ==[]





#test invalid_citation
def test_invalid_citation_is_flagged():
    answer = "Harding and Voss closed the year with revenue of $1.24 billion, up 4.1%. [doc-200]"
    report = grounding.check_citations(answer, SOURCES )
    assert report["passed"] is False

    



# -------------- TESTS FOR CHUNKING ----------------


""" A chunker must not lose, duplicate or mangle text """


import pytest
# file useses it for raises and parameterize 


import chunking 
from documents import DOCUMENTS


#one doc
DOC = next(d for d in DOCUMENTS if d["id"]=="doc-001")
ALL_DOCS = DOCUMENTS

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

def test_plain_sections_carry_no_heading():
    assert not any("> " in c["text"] for c in chunking.by_sections(DOC, contextual=False))

