



# 1.  set up some fake building blocks 
# 2. create a fake model (that keeps going )
# 3. sub in our fakes from step 1 
# 4. hit our endpoint 
# 5. check it stopped 

# pretend the model never stops ...check the code stops it anyways
#4 arbiteray 


from fastapi.testclient import TestClient


import agent 
from main import app 

client = TestClient(app) 


# 1  - BUILDING BLOCKS 



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












