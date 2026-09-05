from backend.app.analysis.contract_analyzer import analyze_contract


def test_contract_analysis_pipeline():
    contract = """
    PAYMENT

    The buyer shall make payment within 30 days of receiving the invoice.

    LIABILITY

    The parties agree to unlimited liability for all damages.

    TERMINATION

    Either party may terminate this agreement by providing written notice.
    """

    result = analyze_contract(contract)

    assert isinstance(result, dict)
    assert "risk_score" in result
    assert "risk_level" in result
    assert "risk_count" in result
    assert "clauses" in result
    assert "risks" in result

    assert isinstance(result["risk_score"], int)
    assert result["risk_score"] >= 0
    assert isinstance(result["clauses"], list)
    assert isinstance(result["risks"], list)

    print("Contract analysis pipeline test passed successfully.")


if __name__ == "__main__":
    test_contract_analysis_pipeline()