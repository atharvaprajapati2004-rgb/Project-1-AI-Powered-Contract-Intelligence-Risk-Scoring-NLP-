from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.analysis.contract_analyzer import analyze_contract
from backend.app.schemas.analysis import ContractAnalysisResponse


router = APIRouter()


class ContractRequest(BaseModel):
    text: str


@router.post(
    "/api/analyze",
    response_model=ContractAnalysisResponse,
)
def analyze_contract_text(request: ContractRequest):
    """
    Analyze contract text.

    Pipeline:
    1. Clause extraction
    2. Risk detection
    3. Risk scoring
    """

    result = analyze_contract(request.text)

    return result