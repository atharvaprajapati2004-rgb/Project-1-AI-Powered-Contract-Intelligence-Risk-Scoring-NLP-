import json
import re
from pathlib import Path


def clean_text(text):
    """Clean and normalize text."""
    if not isinstance(text, str):
        return ""

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def preprocess_cuad(input_file, output_file):
    """Preprocess CUAD JSON dataset."""

    input_path = Path(input_file)
    output_path = Path(output_file)

    # Check input file
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return

    # Load JSON
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        print(f"ERROR: Invalid JSON file: {error}")
        return

    # Check CUAD structure
    if "data" not in data or not isinstance(data["data"], list):
        print("ERROR: Invalid CUAD dataset structure.")
        return

    processed_data = []

    for document in data["data"]:
        document_title = clean_text(document.get("title", ""))

        for paragraph in document.get("paragraphs", []):
            context = clean_text(paragraph.get("context", ""))

            if not context:
                continue

            for qa in paragraph.get("qas", []):
                question = clean_text(qa.get("question", ""))

                answers = qa.get("answers", [])

                if not question:
                    continue

                answer_text = ""

                if answers:
                    answer_text = clean_text(
                        answers[0].get("text", "")
                    )

                processed_data.append(
                    {
                        "document_title": document_title,
                        "context": context,
                        "question": question,
                        "answer": answer_text,
                    }
                )

    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save processed dataset
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            processed_data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("CUAD preprocessing completed successfully.")
    print("=" * 40)
    print(f"Input file : {input_path}")
    print(f"Output file: {output_path}")
    print(f"Records    : {len(processed_data)}")


if __name__ == "__main__":

    input_file = input(
        "Enter CUAD JSON file path: "
    ).strip()

    output_file = "data/processed/cuad_processed.json"

    preprocess_cuad(input_file, output_file)