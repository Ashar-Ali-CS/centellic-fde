
Ashar Ali 
Chosen: candidate-a

Why: I chose candidate-a to submit for production/publication becuase it passed the ruff check,mypy tests and pytests (all 3 of candidates did) . candidate-a  also met ALL spec rules while  the other  reconcile functions did NOT meet all spec rules.


Rejected Candidates:

candidate-b rejected. 
- Why: candidate-b has "running += float(line)" in line 22. Binary Float anywhere is NOT allowed by spec.
- SpecViolation: Rule 1. All arithmetic is exact. A binary float anywhere in the calculation is a defect.
- Consequence: the arthimitic is not exact , that binary float is a defect that could impact system is unknown ways. 

candidate-c  rejected
- Why:  candidate-c has "TOLERENCE = Decimal("0.01")" . This violates the spec rule of no tolerence.
- SpecViolation: Rule 2. `matched` is `True` **only** on an exact zero variance. There is no tolerance. A
   one-penny discrepancy is a discrepancy.
- Consequence: would have given 0.01 variation tolerated in system. when its not supposed to be.

