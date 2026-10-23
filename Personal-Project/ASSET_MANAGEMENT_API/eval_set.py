

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
    # 1. Exact numerical retrieval: management and exit fees
    {
        "question": "What are the annual management fee and exit fee for the ManGuard Class C Fund?",
        "doc_id": "doc-001",
        "evidence": "Fund_Fees: Annual Management Fee 0.75%, Exit Fee 0%",
        "keywords": ["0.75%", "0%"],
        "kind": "exact_numeric_retrieval",
    },

    # 2. Risk rating: preserve the rating and its numerical scale
    {
        "question": "What is the risk rating of the ManGuard Class C Fund?",
        "doc_id": "doc-001",
        "evidence": "Risk_Rating: Low (2/7)",
        "keywords": ["Low", "2/7"],
        "kind": "risk_rating_retrieval",
    },

    # 3. ESG exclusions: distinguish explicit exclusions from general sustainability
    {
        "question": "Which industries does BlueRock Class A Fund exclude, and what is its sustainability mandate?",
        "doc_id": "doc-002",
        "evidence": "ESG: Excludes tobacco and alcohol producers; sustainability-focused mandate",
        "keywords": ["tobacco", "alcohol", "sustainability"],
        "kind": "esg_exclusion_retrieval",
    },

    # 4. Another exact fee question for a similar fund
    {
        "question": "What is the annual management fee and exit fee for BlueRock Class A Fund?",
        "doc_id": "doc-002",
        "evidence": "Fund_Fees: Annual Management Fee 0.85%, Exit Fee 1%",
        "keywords": ["0.85%", "1%"],
        "kind": "similar_fund_numeric_retrieval",
    },

    # 5. Strategy involving multiple concepts in one evidence span
    {
        "question": "What is the investment strategy of FastSaver Pension Fund, including its intended investment horizon and asset exposure?",
        "doc_id": "doc-003",
        "evidence": "Fund_Strategy: Diversified growth strategy designed for long-term pension investing, with exposure to global equities and fixed income",
        "keywords": ["long-term pension", "global equities", "fixed income"],
        "kind": "multi_concept_strategy_retrieval",
    },

    # 6. A similar brand name but a substantially different risk profile
    {
        "question": "What is the risk rating of ManGuard Future Fund?",
        "doc_id": "doc-010",
        "evidence": "Risk_Rating: High (6/7)",
        "keywords": ["High", "6/7"],
        "kind": "similar_name_disambiguation",
    },

    # 7. Strategy and sector focus of ManGuard Future Fund
    {
        "question": "What does ManGuard Future Fund primarily invest in?",
        "doc_id": "doc-010",
        "evidence": "Fund_Strategy: High-growth equity strategy investing primarily in emerging technology and innovative companies",
        "keywords": ["high-growth", "emerging technology", "innovative companies"],
        "kind": "strategy_retrieval",
    },

    # 8. Sustainability without assuming the fund has explicit exclusions
    {
        "question": "Does ManGuard Future Fund have specific ESG exclusions or a sustainability mandate?",
        "doc_id": "doc-010",
        "evidence": "ESG: No specific ESG exclusions or sustainability mandate",
        "keywords": ["no specific", "exclusions", "sustainability mandate"],
        "kind": "negative_fact_retrieval",
    },

    # 9. Manager commentary: investment rationale
    {
        "question": "Why does Jenny consider BlueRock attractive to sustainable investors seeking long-term growth?",
        "doc_id": "doc-004",
        "evidence": "Commentary: BlueRock's sustainability-focused equity strategy remains attractive for investors seeking long-term growth alongside environmental considerations.",
        "keywords": ["sustainability-focused", "long-term growth", "environmental considerations"],
        "kind": "manager_commentary_retrieval",
    },

    # 10. Manager commentary: market risks
    {
        "question": "According to Jenny's commentary, what key risk affects BlueRock's higher-growth holdings?",
        "doc_id": "doc-004",
        "evidence": "Market volatility remains a key risk, particularly for higher-growth holdings.",
        "keywords": ["market volatility", "higher-growth holdings"],
        "kind": "commentary_risk_retrieval",
    },

    # 11. Pension commentary: macroeconomic considerations
    {
        "question": "Which macroeconomic factors does Victor Magnate identify as important for FastSaver's future performance?",
        "doc_id": "doc-009",
        "evidence": "Persistent inflation and changes in interest rates remain important considerations for the portfolio's future performance.",
        "keywords": ["inflation", "interest rates", "future performance"],
        "kind": "long_chunk_commentary_retrieval",
    },

    # 12. Client-specific holdings: multiple allocations
    {
        "question": "What percentages of Jane Turncoat's portfolio are allocated to FastSaver Pension Fund, BlueRock Class A Fund, and Other Assets?",
        "doc_id": "doc-005",
        "evidence": "Portfolio_Allocation: 50 percent FastSaver Pension Fund; 15 percent BlueRock Class A Fund; 35 percent Other Assets",
        "keywords": ["50 percent", "15 percent", "35 percent"],
        "kind": "multi_value_client_retrieval",
    },

    # 13. Client-specific mandate and assets
    {
        "question": "What is Jane Turncoat's total portfolio value?",
        "doc_id": "doc-005",
        "evidence": "Total_Assets: £500,000",
        "keywords": ["£500,000"],
        "kind": "client_numeric_retrieval",
    },

    # 14. Distinguishing one client's holdings from another's
    {
        "question": "Which funds make up Michael Presly's portfolio, and what is the allocation to each?",
        "doc_id": "doc-006",
        "evidence": "Portfolio_Allocation: 50 percent ManGuard Class C Fund; 50 percent FastSaver Pension Fund",
        "keywords": ["50 percent", "ManGuard Class C Fund", "FastSaver Pension Fund"],
        "kind": "client_entity_disambiguation",
    },

    # 15. Client mandate: an explicit restriction
    {
        "question": "What sustainability-related restrictions apply to Jane Turncoat's portfolio?",
        "doc_id": "doc-005",
        "evidence": "Client_Mandate: Sustainability focus; no tobacco exposure",
        "keywords": ["sustainability", "no tobacco exposure"],
        "kind": "client_mandate_retrieval",
    },

    # 16. UNANSWERABLE: no historical performance data is supplied
    {
        "question": "What percentage return did BlueRock Class A Fund achieve over the last 12 months?",
        "doc_id": None,
        "evidence": None,
        "keywords": [],
        "kind": "unanswerable_missing_performance_data",
    },

    # 17. UNANSWERABLE: no fund launch date is supplied
    {
        "question": "On what exact date was FastSaver Pension Fund launched?",
        "doc_id": None,
        "evidence": None,
        "keywords": [],
        "kind": "unanswerable_missing_fund_metadata",
    },

    # 18. UNANSWERABLE: no personal demographic information is supplied
    {
        "question": "How old is Jane Turncoat?",
        "doc_id": None,
        "evidence": None,
        "keywords": [],
        "kind": "unanswerable_missing_client_information",
    },

    # 19. UNANSWERABLE: no income information is supplied
    {
        "question": "What is Linda Langstrom's annual salary?",
        "doc_id": None,
        "evidence": None,
        "keywords": [],
        "kind": "unanswerable_missing_financial_information",
    },

    # 20. UNANSWERABLE: no benchmark comparison or excess return is supplied
    {
        "question": "By how many percentage points did ManGuard Future Fund outperform its benchmark last year?",
        "doc_id": None,
        "evidence": None,
        "keywords": [],
        "kind": "unanswerable_missing_benchmark_data",
    },
]




def answerable() -> list[dict]:
    return [q for q in EVAL_SET if q["doc_id"] is not None]


def unanswerable() -> list[dict]:
    return [q for q in EVAL_SET if q["doc_id"] is None]









