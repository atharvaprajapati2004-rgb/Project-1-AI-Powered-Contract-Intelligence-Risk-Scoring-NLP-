SEVERITY_POINTS = {
    "low": 10,
    "medium": 20,
    "high": 30,
    "critical": 40,
}


def calculate_risk_score(risks):
    """
    Calculate an overall contract risk score from detected risks.

    Parameters:
        risks (list): Risk dictionaries returned by risk_detector.

    Returns:
        dict: Risk score, risk level, and risk count.
    """

    if not isinstance(risks, list):
        return {
            "risk_score": 0,
            "risk_level": "Low",
            "risk_count": 0,
        }

    score = 0

    for risk in risks:
        if not isinstance(risk, dict):
            continue

        severity = str(risk.get("severity", "low")).lower()
        score += SEVERITY_POINTS.get(severity, 0)

    if score >= 81:
        risk_level = "Critical"
    elif score >= 51:
        risk_level = "High"
    elif score >= 21:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "risk_count": len(risks),
    }


if __name__ == "__main__":
    sample_risks = [
        {
            "risk_type": "unlimited_liability",
            "severity": "high",
        },
        {
            "risk_type": "automatic_renewal",
            "severity": "medium",
        },
        {
            "risk_type": "confidentiality_obligation",
            "severity": "medium",
        },
    ]

    result = calculate_risk_score(sample_risks)

    print("Contract Risk Scoring")
    print("=" * 30)
    print(f"Risk Score : {result['risk_score']}")
    print(f"Risk Level : {result['risk_level']}")
    print(f"Risk Count : {result['risk_count']}")