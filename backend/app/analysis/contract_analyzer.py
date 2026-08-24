from backend.app.nlp.clause_extractor import extract_clauses
from backend.app.risk.risk_detector import detect_risks
from backend.app.risk.risk_scorer import calculate_risk_score



def analyze_contract(text):
    """
    Run the complete contract analysis pipeline.

    Pipeline:
        1. Extract clauses
        2. Detect potential risks
        3. Calculate overall risk score
    """

    if not isinstance(text, str) or not text.strip():
        return {
            "risk_score": 0,
            "risk_level": "Low",
            "risk_count": 0,
            "clauses": [],
            "risks": [],
        }

    # Extract contract clauses
    clauses = extract_clauses(text)

    # Detect risks across the complete contract
    risks = detect_risks(text)

    # Calculate overall risk score
    risk_summary = calculate_risk_score(risks)

    return {
        "risk_score": risk_summary["risk_score"],
        "risk_level": risk_summary["risk_level"],
        "risk_count": risk_summary["risk_count"],
        "clauses": clauses,
        "risks": risks,
    }


if __name__ == "__main__":
    sample_contract = """
PAYMENT

The buyer shall make payment within 30 days of receiving the invoice.

CONFIDENTIALITY

Both parties shall maintain confidentiality of all confidential information.

TERMINATION

Either party may terminate this agreement by providing written notice.

LIABILITY

The parties agree to unlimited liability for all damages.

RENEWAL

The agreement shall automatically renew for another year.
"""

    result = analyze_contract(sample_contract)

    print("Contract Analysis Pipeline")
    print("=" * 40)

    print(f"Risk Score : {result['risk_score']}")
    print(f"Risk Level : {result['risk_level']}")
    print(f"Risk Count : {result['risk_count']}")

    print("\nDetected Clauses")
    print("-" * 40)

    for clause in result["clauses"]:
        print(f"{clause['clause_id']}. {clause['clause_type']}")

    print("\nDetected Risks")
    print("-" * 40)

    for risk in result["risks"]:
        print(
            f"{risk['risk_type']} | "
            f"{risk['severity']} | "
            f"{risk['matched_text']}"
        )