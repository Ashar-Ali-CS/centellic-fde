


# Chunking decision

**Date:23/10/2026**   **Decided by:** ASHAR ALI   **Corpus:** documents.py
**Eval set:** eval_set.py  **Embedding model:** voyage-3-lite

## Decision
We serve `whole document` strategy  with a relevance floor of `0.4`.




## Evidence


To evalute the chunking strategies and which is best I ran eval retrieva -
venv/Scripts/python.exe -m eval_retrieval - in git bash. I found this : 



Embedded 20 questions once (283 tokens), reused for every strategy.

strategy                 R@1   R@3   R@5    MRR  ctx words  top ans  top unans
------------------------------------------------------------------------------
whole_document          0.93  1.00  1.00   0.97        113     0.69       0.56
fixed_100               0.93  1.00  1.00   0.97        113     0.69       0.56
fixed_overlap_25        0.93  1.00  1.00   0.97        113     0.69       0.56
sentences_100           0.93  1.00  1.00   0.97        113     0.69       0.56
sections_plain          0.93  1.00  1.00   0.97        113     0.69       0.56
sections_contextual     0.93  1.00  1.00   0.97        125     0.67       0.55

Missed at k=3:
  whole_document         none
  fixed_100              none
  fixed_overlap_25       none
  sentences_100          none
  sections_plain         none
  sections_contextual    none


WHen i ran eval answers i found with current relevence floors : 

floor = 0.4

strategy                answers  refusals  calls  avg in tokens
whole_document             0.93      1.00     20            100
    false refusals: none
    wrong or not refused: unknown






## Why this one
<Two or three sentences. Which number decided it, and what you gave up.>

I chosee whole document strategy as i saw that chunking  methods didnt improve performance .

Furthermore , I chose the floor  0.4 , it is low- I saw the answer accuracy was high and there was no false refusals. 


However,what i gave up was the relevence floor being high enough to ignore unaswerable queries - all 20 questions in eval set led to model call. Even though 5 where unanswerable .


## Known weaknesses
<Questions the winner still misses, by kind. Which ones need hybrid retrieval, not better chunking?>


Currently my data/documents are not to extensive and structured. Later on I might need a better chunking strategy ,such as when documents with secitons(titles/headers) come. 

My relevence floor is also quite low and should be increased to avoid making too many model calls. 



## Revisit when
<What would make this decision wrong: a new document type, a new embedding model, longer documents.>


We should revisit this descision , when there is new document type that is more structured i.e split into title +headers.
Sections contextual uses "## " header parts in the document could  help chunk it. 

Furthermore , the descision should also be re-evaluted when there is longer documents. This could impact token counts and we may want to increase relevence floor. 

