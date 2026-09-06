from backend.app.tasks.contract_tasks import analyze_contract_task


def test_celery_contract_analysis_task():
    contract = """
    PAYMENT

    The buyer must pay within 30 days.

    LIABILITY

    The parties agree to unlimited liability.
    """

    result = analyze_contract_task.apply(args=[contract])

    data = result.get()

    assert isinstance(data, dict)
    assert "risk_score" in data
    assert "risk_level" in data
    assert "risk_count" in data
    assert data["risk_score"] == 30
    assert data["risk_level"] == "Medium"

    print("Celery contract analysis task test passed successfully.")