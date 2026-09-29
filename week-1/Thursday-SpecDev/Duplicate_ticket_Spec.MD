## Spec for creating  "merge_same_ticket" function

WHY  - Customers often raise the same problem. We need to merge duplicate tickets to reduce support workload and keep discussion in a single ticket.

WHAT - Implement merge_same_ticket to identify tickets with the same subject and merge them into a single ticket.

CONTEXT - 
File: tickets.py
Pattern: one line docstring
Settled: merged issue remains in the surviving ticket record

CONSTRAINTS - Out of Scope: Not emailing customer , Avoid new dependencies, Change existing functions

TASKS  - 

Task 1 :Normalise Subjects to lower case
 Touches:
 Verify:"Can't Login" and "can't login" are treated as the same subject.


Task 2: Identify Duplicate Tickets
 Touches: tickets.py
 Verify: Tickets with matching normalized subjects are identified as duplicates, Tickets with different subjects are ignored

Task 3 : Select Primary Ticket
Touches: tickets.py
Verify: The oldest ticket (earliest created_at) is retained, Only one primary ticket exists per subjec

Task 4: Merge Duplicate Tickets
Touches: tickets.py
Verify: Duplicate tickets are removed from the returned list, Only one ticket remains for each subject