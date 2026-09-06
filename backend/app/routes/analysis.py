from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.analysis.contract_analyzer import analyze_contract
from backend.app.schemas.analysis import ContractAnalysisResponse
from backend.app.tasks.contract_tasks import analyze_contract_task


router = APIRouter()


class ContractRequest(BaseModel):
    text: str


class TaskResponse(BaseModel):
    task_id: str
    status: str


@router.post(
    "/api/analyze",
    response_model=ContractAnalysisResponse,
)
def analyze_contract_text(request: ContractRequest):
    """
    Analyze contract text synchronously.

    Pipeline:
    1. Clause extraction
    2. Risk detection
    3. Risk scoring
    """

    result = analyze_contract(request.text)

    return result


@router.post(
    "/api/analyze/background",
    response_model=TaskResponse,
)
def analyze_contract_background(request: ContractRequest):
    """
    Submit contract analysis as a Celery background task.
    """

    task = analyze_contract_task.delay(request.text)

    return {
        "task_id": task.id,
        "status": "submitted",
    }