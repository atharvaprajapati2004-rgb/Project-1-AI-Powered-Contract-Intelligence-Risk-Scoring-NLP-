from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.analysis.contract_analyzer import analyze_contract


router = APIRouter(
    prefix="/api",
    tags=["Contract Analysis"],
)


class ContractAnalysisRequest(BaseModel):
    text: str


@router.post("/analyze")
def analyze_contract_endpoint(request: ContractAnalysisRequest):
    """
    Analyze contract text and return clauses, risks, and risk score.
    """

    return analyze_contract(request.text)