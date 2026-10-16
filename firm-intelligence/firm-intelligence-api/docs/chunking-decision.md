


# Chunking decision

**Date:** 13/10/2026  **Decided by:** ASHAR ALI   **Corpus:** documents.py + corpus.py (16 documents)
**Eval set:** eval_set.py (29 answerable, 3 unanswerable)  **Embedding model:** voyage-3-lite

## Decision
We serve `sections_contextual` with a relevance floor of `<floor>`.



## Evidence


Note - Answer acc+ refusal acc aquired through using running "eval_answers" for these strategies in git bash



| Strategy | R@1 | R@3 | MRR | Context words@3 | Answer acc. | Refusal acc. |
|---|---|---|---|---|---|---|
| whole_document|0.69|1.0|0.84| 862| 0.97 | 1.00|
| <best>sections_contextual |0.86 | 1.00 | 0.93 | 197 | 0.79 | 1.00 |
| <second>fixed_overlap_25| 0.52| 0.97 |0.67 |277 | 0.97 | 1.00 |




## Why this one
<Two or three sentences. Which number decided it, and what you gave up.>

I choose sections_contextual as it performed better in the metrics - MRR , R@1 and R@3 - then compared to the whole_document baseline and other strategies.

Furthermore , I chose the floor 0.55 as optimal point becuase after testing it on running eval answers on differnt floor levels i found that it leads to too many false refusals(answerable question being rejected by model) or calling model for unanswerable answers (theres 32 documents and 3 are unanswerable). So if it only makes 29 calls its indicative that the model. 




EVIDENCE 0.55 IS GOOD DESCION -  0.55  catches the third unanswerable(32 calls but only calls model for the answerable 29 which saves cost + tokens ) but also cuases more false refusals (3) compared to going below

$ .venv/Scripts/python.exe -m eval_answers sections_contextual --floor 0.55
floor = 0.55

strategy                answers  refusals  calls  avg in tokens
sections_contextual        0.90      1.00     29            315
    false refusals: q06, q09, q24
    wrong or not refused: none




 
WHY BAD BELOW 0.55 to 0.50  - Goes back up to 30 calls which means it called model to  answer a question that was unanswerable. This is ineffecincy.  Even if there is less false refusals

$ .venv/Scripts/python.exe -m eval_answers sections_contextual --floor 0.50
floor = 0.5

strategy                answers  refusals  calls  avg in tokens
sections_contextual        0.97      1.00     30            379
    false refusals: q24
    wrong or not refused: none




WHY BAD ABOVE 0.55 to 0.60 - leads to a large amount of false refusals (twice the number). Also doesnt call model as much for even correct answers(26)
$ .venv/Scripts/python.exe -m eval_answers sections_contextual --floor 0.60
floor = 0.6

strategy                answers  refusals  calls  avg in tokens
sections_contextual        0.76      1.00     26            249
    false refusals: q06, q09, q10, q12, q14, q16, q24
    wrong or not refused: none




## Known weaknesses
<Questions the winner still misses, by kind. Which ones need hybrid retrieval, not better chunking?>


question 24 -  It was answerable but scores very low . However, when it was retrived its still cuasing refusal my model. This is becuase the sementic retrivel finds the keyword/document but it does not directly answer what the question was answering.  Some questions like this are better served with a hybrid retrivel approach. 



## Revisit when
<What would make this decision wrong: a new document type, a new embedding model, longer documents.>


We should revisit this descision , when there is new document type that is less structured i.e not split into title +headers.
Sections contextual uses "## " header parts in the document to help chunk it. 

Furthermore , the descision should also be re-evaluted when there is longer documents. This could impact token counts and we may want to decreasse relevence floor. 

