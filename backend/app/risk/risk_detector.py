import re


RISK_PATTERNS = {
    "unlimited_liability": {
        "patterns": [
            r"unlimited liability",
            r"unlimited liabilities",
            r"liable for all damages",
        ],
        "severity": "high",
        "description": "The clause may expose a party to broad or unlimited liability.",
    },
    "broad_indemnification": {
        "patterns": [
            r"indemnify and hold harmless",
            r"indemnify.*against all",
            r"indemnification.*all claims",
        ],
        "severity": "high",
        "description": "The clause may create broad indemnification obligations.",
    },
    "automatic_renewal": {
        "patterns": [
            r"automatically renew",
            r"automatic renewal",
            r"shall automatically renew",
        ],
        "severity": "medium",
        "description": "The agreement may renew automatically unless notice is provided.",
    },
    "termination_restriction": {
        "patterns": [
            r"may not terminate",
            r"cannot terminate",
            r"no right to terminate",
        ],
        "severity": "high",
        "description": "The clause may restrict a party's ability to terminate the agreement.",
    },
    "confidentiality_obligation": {
        "patterns": [
            r"confidential information",
            r"confidentiality obligations",
            r"shall maintain confidentiality",
        ],
        "severity": "medium",
        "description": "The clause contains confidentiality obligations.",
    },
    "payment_obligation": {
        "patterns": [
            r"payment within \d+ days",
            r"late payment",
            r"payment obligation",
        ],
        "severity": "medium",
        "description": "The clause contains payment-related obligations or conditions.",
    },
}


def detect_risks(text):
    """
    Detect potential contractual risk indicators in a text.

    Returns a list of detected risks with their type,
    severity, matched text, and explanation.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    detected_risks = []
    text_lower = text.lower()

    for risk_type, risk_info in RISK_PATTERNS.items():
        for pattern in risk_info["patterns"]:
            match = re.search(pattern, text_lower)

            if match:
                detected_risks.append(
                    {
                        "risk_type": risk_type,
                        "severity": risk_info["severity"],
                        "matched_text": match.group(0),
                        "description": risk_info["description"],
                    }
                )
                break

    return detected_risks


if __name__ == "__main__":
    sample_clause = """
    The parties shall indemnify and hold harmless each other
    against all claims arising from this agreement.
    The agreement shall automatically renew for another year.
    """

    risks = detect_risks(sample_clause)

    print("Contract Risk Indicator Detection")
    print("=" * 40)

    if not risks:
        print("No potential risk indicators detected.")
    else:
        for risk in risks:
            print(f"\nRisk Type : {risk['risk_type']}")
            print(f"Severity  : {risk['severity']}")
            print(f"Matched   : {risk['matched_text']}")
            print(f"Reason    : {risk['description']}")