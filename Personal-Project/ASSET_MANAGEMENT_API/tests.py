

# Tests with the LLM and embedding calls mocked.
#  Cover at least the summary, the refusal rule and the agent loop, including the iteration limit.




import anthropic
from fastapi.testclient import TestClient

import llm
from main import app


client = TestClient(app)




# FAKE SUMMARY OF CLIENT PORTFOLIO 1 

FAKE_SUMMARY = {
    "id": 1, "name": "Harding & Voss", "summary": "A fixture company",
    "input_tokens": 120, "output_tokens": 95, "stop_reason": "end_turn"
    }

# TESTS FOR LLM 




def test_summary_returns_text_and_summary(monkeypatch):
    monkeypatch.setattr(llm, "summarise_firm", lambda firm: FAKE_SUMMARY)
    response = client.post("/por/1/summary")
    #assert what it should do 
    assert response.status_code ==200
    assert response.json()["input_tokens"] == 120