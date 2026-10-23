


# Chunking decision

**Date:**   **Decided by:** ASHAR ALI   **Corpus:** documents.py
**Eval set:** eval_set.py (, 3 )  **Embedding model:** voyage-3-lite

## Decision
We serve `<strategy>` with a relevance floor of `<floor>`.



## Evidence


Note - Answer acc+ refusal acc aquired through using running "eval_answers" for these strategies in git bash



| Strategy | R@1 | R@3 | MRR | Context words@3 | Answer acc. | Refusal acc. |
|---|---|---|---|---|---|---|
| whole_document|0.69|1.0|0.84| 862| 0.97 | 1.00|
| <best>sections_contextual |0.86 | 1.00 | 0.93 | 197 | 0.79 | 1.00 |
| <second>fixed_overlap_25| 0.52| 0.97 |0.67 |277 | 0.97 | 1.00 |




## Why this one
<Two or three sentences. Which number decided it, and what you gave up.>

I choose ?>>> as it performed better in the metrics - MRR , R@1 and R@3 - then compared to the whole_document baseline and other strategies.

Furthermore , I chose the floor ?? as optimal point becuase after testing it on running eval answers on differnt floor levels i found that it leads to too many false refusals(answerable question being rejected by model) or calling model for unanswerable answers (theres 32 documents and 3 are unanswerable). So if it only makes 29 calls its indicative that the model. 




EVIDENCE 0.55 IS GOOD DESCION - 



 
WHY BAD BELOW 0.55 to 0.50  



WHY BAD ABOVE 0.55 to 0.60 -



## Known weaknesses
<Questions the winner still misses, by kind. Which ones need hybrid retrieval, not better chunking?>





## Revisit when
<What would make this decision wrong: a new document type, a new embedding model, longer documents.>


We should revisit this descision , when there is new document type that is less structured i.e not split into title +headers.
Sections contextual uses "## " header parts in the document to help chunk it. 

Furthermore , the descision should also be re-evaluted when there is longer documents. This could impact token counts and we may want to decreasse relevence floor. 

