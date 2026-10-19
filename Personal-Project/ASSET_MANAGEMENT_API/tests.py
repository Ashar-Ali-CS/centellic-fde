

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



