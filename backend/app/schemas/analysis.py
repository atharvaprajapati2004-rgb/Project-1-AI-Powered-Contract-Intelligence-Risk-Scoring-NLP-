from typing import Any

from pydantic import BaseModel, Field


class ContractAnalysisResponse(BaseModel):
    risk_score: int = Field(default=0, ge=0)
    risk_level: str = "Low"
    risk_count: int = Field(default=0, ge=0)
    clauses: list[dict[str, Any]] = Field(default_factory=list)
    risks: list[dict[str, Any]] = Field(default_factory=list)
    entities: list[dict[str, Any]] = Field(default_factory=list)


class FileAnalysisResponse(BaseModel):
    filename: str
    file_type: str
    extracted_characters: int = Field(default=0, ge=0)
    analysis: ContractAnalysisResponse