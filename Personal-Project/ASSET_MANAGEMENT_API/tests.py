

# Tests with the LLM and embedding calls mocked.
#  Cover at least the summary, the refusal rule and the agent loop, including the iteration limit.




import anthropic
from fastapi.testclient import TestClient


import knowledge_store as knowledge

from main import app

import llm


client = TestClient(app)




# FAKE SUMMARY OF CLIENT PORTFOLIO 1 

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









#NOT IMPLEMENTED YET : 

# ----------- TESTS FOR VECTOR SEARCH EMBEDDINGS (no real embedding calls) --------------

#def test_search_returns_ranked_hits(monkeypatch):
#    monkeypatch.setattr(knowledge, "search", lambda q, k=3: [STRONG_HIT])

#    response = client.post("/knowledge/search", json={"question": "how is PEP worked out"})
#    assert response.status_code == 200
#    assert response.json()["results"][0]["id"] == "doc-008"


# TESTING INDEX BUILT BEFORE
#def test_search_before_indexing_is_409(monkeypatch):
 #   def not_built(q, k=3):
 #       return 409

 #   monkeypatch.setattr(knowledge, "search", not_built)

 #   response = client.post("/knowledge/search", json={"question": "anything at all"})
#    assert response.status_code == 409



#TESTING REFUSAL RULE 

#def test_ask_refuses_without_calling_the_model(monkeypatch):
#    monkeypatch.setattr(knowledge, "search", lambda q, k=3: [WEAK_HIT])

  #  def must_not_be_called(q, c):
  #      raise AssertionError("The model was called despite no relevant context")

   # monkeypatch.setattr(llm, "answer_from_context", must_not_be_called)

    #body = client.post("/knowledge/ask", json={"question": "what is the capital of France"}).json()
    #assert body["refused"] is True
    #assert body["answer"] is None
    #assert body["sources"] == []


def test_short_question_is_rejected_before_any_work():
    assert client.post("/knowledge/ask", json={"question": "hi"}).status_code == 422






# ----------- TESTS FOR AGENT AND MAX ITERATIONS --------------




#need to do this