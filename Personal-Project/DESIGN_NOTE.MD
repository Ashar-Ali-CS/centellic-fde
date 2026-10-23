

# Design Note 



- Why did you set your relevance floor where you did, and what happened when you tried other values?

I set the relevence floor to 0.4. I did not try other values as yet (see chunking_descision.MD) but this needs to be further explored. 



- Would you chunk your documents? Why or why not, given their length and shape?


I would not chunk my documents right now. This is due to thier length (not really long content). Also due to thier unstructured nature(no sections+titles). I also evaluted chunking strategies and found it didnt improve metrics like recall k and mrr. (see chunking_descision.MD) 




- What is the worst wrong answer your system could give, and what stops it?


The worst wrong answer would be providing incorrect financial information or recommending an unsuitable fund to a client, potentially leading to poor investment decisions. For example, the system could incorrectly claim that a fund meets a client's ESG restrictions or provide an unsupported prediction of portfolio returns.

Currently, the system uses retrieval to ground responses in the available documents and a relevance floor to determine whether retrieved information is passed to the language model. However, the top_k is 3 which should go up to 5. Furthermore,  these measures do not guarantee that every answer is correct or prevent all unsupported claims. Further evaluation of unanswerable questions, relevance-floor tuning, and validation of tool outputs would help reduce these risks. The system should clearly state when information is unavailable rather than inventing an answer.