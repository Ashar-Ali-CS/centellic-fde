
Ashar Ali 

Note- I also  tested all 3 candidates on git bash using cd to each one than "cd .." to go back. Each candidate passed  the ruff check,mypy tests and pytests .

Chosen: candidate-a

Why: I chose candidate-a to submit for production/publication becuase it met ALL spec rules while  the other  functions did NOT meet all spec rules.

Rejected Candidates:

1.candidate-b rejected. 
- Why: candidate-b has "running += float(line)" in line 22. Binary Float anywhere is NOT allowed by spec.
- SpecViolation: Rule 1. All arithmetic is exact. A binary float anywhere in the calculation is a defect.
- Consequence: the arthmitic might not be exact or will be calculate to wrong decimal. It is a defect that could impact system by  potentially wrong calculation of variance or other errors.

2.candidate-c  rejected
- Why:  candidate-c has "TOLERENCE = Decimal("0.01")" . This violates the spec rule of no tolerence.
- SpecViolation: Rule 2. `matched` is `True` **only** on an exact zero variance. There is no tolerance. A
   one-penny discrepancy is a discrepancy.
- Consequence: would have given 0.01 variation tolerated in system. when its not supposed to be.

