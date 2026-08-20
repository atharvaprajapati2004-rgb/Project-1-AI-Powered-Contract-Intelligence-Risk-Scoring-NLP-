import re


CLAUSE_PATTERNS = {
    "termination": [
        r"\btermination\b",
        r"\bterminate\b",
        r"\bterminated\b",
    ],
    "confidentiality": [
        r"\bconfidentiality\b",
        r"\bconfidential\b",
        r"\bnon[- ]disclosure\b",
    ],
    "payment": [
        r"\bpayment\b",
        r"\bpayments\b",
        r"\bpayable\b",
        r"\binvoice\b",
    ],
    "liability": [
        r"\bliability\b",
        r"\bliabilities\b",
        r"\blimitation of liability\b",
    ],
    "indemnification": [
        r"\bindemnification\b",
        r"\bindemnify\b",
        r"\bindemnity\b",
    ],
    "governing_law": [
        r"\bgoverning law\b",
        r"\bapplicable law\b",
    ],
    "intellectual_property": [
        r"\bintellectual property\b",
        r"\bip rights\b",
        r"\bcopyright\b",
        r"\btrademark\b",
    ],
    "renewal": [
        r"\brenewal\b",
        r"\brenew\b",
        r"\bautomatically renew\b",
    ],
    "dispute_resolution": [
        r"\bdispute resolution\b",
        r"\barbitration\b",
        r"\bmediation\b",
        r"\bdisputes\b",
    ],
}


def identify_clause_type(text):
    """
    Identify the most likely contract clause type.
    """

    if not isinstance(text, str):
        return "unknown"

    text_lower = text.lower()

    for clause_type, patterns in CLAUSE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return clause_type

    return "unknown"


def extract_clauses(text):
    """
    Extract potential contract clauses from text.

    The text is split into paragraphs/sections and each section
    is assigned a likely clause category.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    sections = re.split(r"\n\s*\n+", text.strip())

    clauses = []

    for index, section in enumerate(sections, start=1):
        section = section.strip()

        if not section:
            continue

        clause_type = identify_clause_type(section)

        clauses.append(
            {
                "clause_id": index,
                "clause_type": clause_type,
                "text": section,
            }
        )

    return clauses


if __name__ == "__main__":
    sample_contract = """
PAYMENT

The buyer shall make payment within 30 days of receiving the invoice.

CONFIDENTIALITY

Both parties shall maintain confidentiality of all confidential information.

TERMINATION

Either party may terminate this agreement by providing written notice.

GOVERNING LAW

This agreement shall be governed by the applicable law.
"""

    extracted_clauses = extract_clauses(sample_contract)

    print("Contract Clause Extraction")
    print("=" * 40)

    for clause in extracted_clauses:
        print(f"\nClause ID   : {clause['clause_id']}")
        print(f"Clause Type : {clause['clause_type']}")
        print(f"Text        : {clause['text']}")