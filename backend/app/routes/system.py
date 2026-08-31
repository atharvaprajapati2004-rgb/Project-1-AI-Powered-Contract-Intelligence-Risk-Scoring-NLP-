from fastapi import APIRouter


router = APIRouter()


@router.get("/api/health")
def health_check():
    """
    Check whether the Contract Intelligence API is running.
    """

    return {
        "status": "healthy",
        "service": "Contract Intelligence API",
    }


@router.get("/api/info")
def project_info():
    """
    Return basic information about the project and
    currently supported analysis features.
    """

    return {
        "project": "AI-Powered Contract Intelligence",
        "version": "1.0.0",
        "supported_file_types": [
            "TXT",
            "PDF",
            "DOCX",
        ],
        "analysis_features": [
            "Clause Extraction",
            "Risk Detection",
            "Risk Scoring",
        ],
    }