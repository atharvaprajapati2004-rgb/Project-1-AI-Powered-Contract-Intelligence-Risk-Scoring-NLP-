from backend.app.nlp.clause_extractor import extract_clauses
from backend.app.nlp.ner_extractor import extract_entities
from backend.app.risk.risk_detector import detect_risks
from backend.app.risk.risk_scorer import calculate_risk_score


def analyze_contract(text):
    """
    Run the complete contract analysis pipeline.

    Pipeline:
        1. Extract named entities
        2. Extract clauses
        3. Detect potential risks
        4. Calculate overall risk score
    """
    if not isinstance(text, str) or not text.strip():
        return {
            "risk_score": 0,
            "risk_level": "Low",
            "risk_count": 0,
            "clauses": [],
            "risks": [],
            "entities": [],
        }

    entities = extract_entities(text)
    clauses = extract_clauses(text)
    risks = detect_risks(text)
    risk_summary = calculate_risk_score(risks)

    return {
        "risk_score": risk_summary["risk_score"],
        "risk_level": risk_summary["risk_level"],
        "risk_count": risk_summary["risk_count"],
        "clauses": clauses,
        "risks": risks,
        "entities": entities,
    }