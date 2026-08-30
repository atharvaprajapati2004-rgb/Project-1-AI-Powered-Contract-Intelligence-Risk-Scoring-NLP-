from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.app.analysis.contract_analyzer import analyze_contract
from backend.app.schemas.analysis import FileAnalysisResponse
from backend.app.utils.document_loader import load_contract


router = APIRouter()


ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}


@router.post(
    "/api/analyze-file",
    response_model=FileAnalysisResponse,
)
async def analyze_contract_file(file: UploadFile = File(...)):
    """
    Upload a TXT, PDF, or DOCX contract and analyze it.
    """

    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload TXT, PDF, or DOCX.",
        )

    temporary_path = None

    try:
        file_data = await file.read()

        if not file_data:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty.",
            )

        with NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temporary_file:
            temporary_file.write(file_data)
            temporary_path = temporary_file.name

        extracted_text = load_contract(temporary_path)

        analysis_result = analyze_contract(extracted_text)

        return {
            "filename": file.filename,
            "file_type": extension.replace(".", "").upper(),
            "extracted_characters": len(extracted_text),
            "analysis": analysis_result,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Contract file analysis failed: {error}",
        )

    finally:
        if temporary_path:
            temporary_file_path = Path(temporary_path)

            if temporary_file_path.exists():
                temporary_file_path.unlink()