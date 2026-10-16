

import grounding 

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