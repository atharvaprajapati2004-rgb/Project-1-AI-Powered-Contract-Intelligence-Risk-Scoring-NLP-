import json
from pathlib import Path


def validate_cuad(file_path):
    path = Path(file_path)

    # Check whether the file exists
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        return

    # Load and validate JSON
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        print(f"ERROR: Invalid JSON file: {error}")
        return

    print("CUAD Dataset Validation")
    print("=" * 30)

    # Check main data field
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

    warnings = 0

    # Validate documents
    for document_index, document in enumerate(documents, start=1):

        if "title" not in document:
            print(f"WARNING: Document {document_index} is missing 'title'.")
            warnings += 1

        if "paragraphs" not in document:
            print(
                f"WARNING: Document {document_index} is missing 'paragraphs'."
            )
            warnings += 1
            continue

        paragraphs = document["paragraphs"]

        if not isinstance(paragraphs, list):
            print(
                f"WARNING: Document {document_index} "
                "'paragraphs' should be a list."
            )
            warnings += 1
            continue

        total_paragraphs += len(paragraphs)

        # Validate paragraphs
        for paragraph_index, paragraph in enumerate(
            paragraphs, start=1
        ):

            if "context" not in paragraph:
                print(
                    f"WARNING: Document {document_index}, "
                    f"Paragraph {paragraph_index} is missing 'context'."
                )
                warnings += 1

            if "qas" not in paragraph:
                print(
                    f"WARNING: Document {document_index}, "
                    f"Paragraph {paragraph_index} is missing 'qas'."
                )
                warnings += 1
                continue

            qas = paragraph["qas"]

            if not isinstance(qas, list):
                print(
                    f"WARNING: Document {document_index}, "
                    f"Paragraph {paragraph_index} 'qas' should be a list."
                )
                warnings += 1
                continue

            # Validate questions and answers
            for question_index, qa in enumerate(qas, start=1):
                total_questions += 1

                if "question" not in qa:
                    print(
                        f"WARNING: Document {document_index}, "
                        f"Paragraph {paragraph_index}, "
                        f"Question {question_index} is missing 'question'."
                    )
                    warnings += 1

                if "answers" not in qa:
                    print(
                        f"WARNING: Document {document_index}, "
                        f"Paragraph {paragraph_index}, "
                        f"Question {question_index} is missing 'answers'."
                    )
                    warnings += 1
                    continue

                answers = qa["answers"]

                if not isinstance(answers, list):
                    print(
                        f"WARNING: Document {document_index}, "
                        f"Paragraph {paragraph_index}, "
                        f"Question {question_index} "
                        "'answers' should be a list."
                    )
                    warnings += 1
                    continue

                total_answers += len(answers)

    # Print summary
    print("\nDataset Summary")
    print("-" * 30)
    print(f"Documents : {len(documents)}")
    print(f"Paragraphs: {total_paragraphs}")
    print(f"Questions : {total_questions}")
    print(f"Answers   : {total_answers}")
    print(f"Warnings  : {warnings}")

    if warnings == 0:
        print("\nValidation completed successfully.")
        print("No structural issues found.")
    else:
        print("\nValidation completed with warnings.")


if __name__ == "__main__":
    dataset_path = input("Enter CUAD JSON file path: ").strip()

    validate_cuad(dataset_path)