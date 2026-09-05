"""
Contract document loading utility.

Supports:
- TXT files
- PDF files
- DOCX files

The extracted text can be passed to the
Contract Analysis Pipeline.
"""

from pathlib import Path


def load_txt(file_path: str) -> str:
    """Extract text from a TXT file."""
    path = Path(file_path)

    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def load_pdf(file_path: str) -> str:
    """Extract text from a PDF, using OCR for scanned PDFs."""
    import fitz
    import pytesseract
    from pdf2image import convert_from_path

    path = Path(file_path)

    document = fitz.open(path)

    pages = []

    for page in document:
        text = page.get_text().strip()
        if text:
            pages.append(text)

    document.close()

    extracted_text = "\n".join(pages).strip()

    # If normal PDF extraction worked, return the text.
    if extracted_text:
        return extracted_text

    # Otherwise, treat the PDF as a scanned document and use OCR.
    images = convert_from_path(str(path), dpi=200)

    ocr_pages = []

    for image in images:
        text = pytesseract.image_to_string(image).strip()
        if text:
            ocr_pages.append(text)

    return "\n".join(ocr_pages)


def load_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    from docx import Document

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def load_contract(file_path: str) -> str:
    """
    Load a contract document and return its extracted text.

    Supported formats:
    .txt
    .pdf
    .docx
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Contract file not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension == ".txt":
        text = load_txt(file_path)

    elif extension == ".pdf":
        text = load_pdf(file_path)

    elif extension == ".docx":
        text = load_docx(file_path)

    else:
        raise ValueError(
            "Unsupported file format. "
            "Supported formats are: TXT, PDF, DOCX."
        )

    if not text.strip():
        raise ValueError(
            "The contract document does not contain readable text."
        )

    return text


if __name__ == "__main__":
    file_path = input("Enter contract file path: ").strip()

    try:
        extracted_text = load_contract(file_path)

        print("=" * 60)
        print("CONTRACT DOCUMENT LOADER")
        print("=" * 60)

        print(f"\nFile: {file_path}")
        print(f"Extracted characters: {len(extracted_text)}")

        print("\nExtracted text preview:")
        print("-" * 60)
        print(extracted_text[:1000])

        print("\n" + "=" * 60)
        print("DOCUMENT LOADING COMPLETED")
        print("=" * 60)

    except Exception as error:
        print(f"\nERROR: {error}")