

"""A labelled eval set for retrieval and answer quality.

Each answerable question records:
  doc_id    the document that holds the answer
  evidence  a short verbatim span from that document. A retrieved chunk counts as a hit
            only if it contains this exact span, so a chunk that cuts the span in half
            is a miss. That is deliberate: it is how chunking damage shows up in the numbers.
  keywords  what a correct answer must mention. Every item must appear in the answer.
            "a|b" means either a or b is acceptable. Matching is case-insensitive and
            whole-word, so "no" does not match inside "not". A trailing * allows any
            ending, so "exclud*" matches "excluded" and "excludes". A refusal never
            counts as correct, whatever words it happens to contain.
  kind      what the question tests

Unanswerable questions have doc_id None and no evidence. The correct behaviour is refusal.
"""

EVAL_SET = [
    
]


def answerable() -> list[dict]:
    return [q for q in EVAL_SET if q["doc_id"] is not None]


def unanswerable() -> list[dict]:
    return [q for q in EVAL_SET if q["doc_id"] is None]









