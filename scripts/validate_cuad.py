import json
from pathlib import Path


def validate_cuad(file_path):
    path = Path(file_path)

    if not path.exists():
        print(f"ERROR: File not found: {path}")
        return

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        print(f"ERROR: Invalid JSON file: {error}")
        return

    print("CUAD Dataset Validation")
    print("=" * 30)

    if "data" not in data:
        print("ERROR: Missing 'data' field.")
        return

    documents = data["data"]

    if not isinstance(documents, list):
        print("ERROR: 'data' should be a list.")
        return

    total_paragraphs = 0
    total_questions = 0
    total_answers = 0

    for document in documents:
        paragraphs = document.get("paragraphs", [])

        total_paragraphs += len(paragraphs)

        for paragraph in paragraphs:
            for qa in paragraph.get("qas", []):
                total_questions += 1
                total_answers += len(qa.get("answers", []))

    print(f"Documents : {len(documents)}")
    print(f"Paragraphs: {total_paragraphs}")
    print(f"Questions : {total_questions}")
    print(f"Answers   : {total_answers}")

    print("\nValidation completed successfully.")


if __name__ == "__main__":
    dataset_path = input("Enter CUAD JSON file path: ").strip()

    validate_cuad(dataset_path)