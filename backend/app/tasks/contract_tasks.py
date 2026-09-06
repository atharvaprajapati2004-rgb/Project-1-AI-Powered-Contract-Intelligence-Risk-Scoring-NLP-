from backend.app.analysis.contract_analyzer import analyze_contract
from backend.app.tasks.celery_app import celery_app


@celery_app.task(name="analyze_contract_task")
def analyze_contract_task(text: str):
    """Run contract analysis as a background task."""
    return analyze_contract(text)