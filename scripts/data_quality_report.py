import json
from pathlib import Path
from collections import Counter


def generate_quality_report(file_path):
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

    if "data" not in data or not isinstance(data["data"], list):
        print("ERROR: Invalid CUAD dataset structure.")
        return

    documents = data["data"]

    empty_documents = 0
    empty_paragraphs = 0
    empty_questions = 0
    questions_without_answers = 0
    answers_without_text = 0
    question_ids = []

    total_paragraphs = 0
    total_questions = 0
    total_answers = 0

    for document in documents:

        if not document.get("paragraphs"):
            empty_documents += 1

        for paragraph in document.get("paragraphs", []):
            total_paragraphs += 1

            if not paragraph.get("context", "").strip():
                empty_paragraphs += 1

            for qa in paragraph.get("qas", []):
                total_questions += 1

                question_ids.append(qa.get("id", ""))

                if not qa.get("question", "").strip():
                    empty_questions += 1

                answers = qa.get("answers", [])

                if not answers:
                    questions_without_answers += 1

                for answer in answers:
                    total_answers += 1

                    if not answer.get("text", "").strip():
                        answers_without_text += 1

    duplicate_ids = sum(
        count - 1
        for count in Counter(question_ids).values()
        if count > 1 and count > 1
    )

    print("\nCUAD Data Quality Report")
    print("=" * 35)

    print(f"Documents              : {len(documents)}")
    print(f"Paragraphs             : {total_paragraphs}")
    print(f"Questions              : {total_questions}")
    print(f"Answers                : {total_answers}")

    print("\nPotential Data Quality Issues")
    print("-" * 35)

    print(f"Empty documents        : {empty_documents}")
    print(f"Empty paragraphs       : {empty_paragraphs}")
    print(f"Empty questions        : {empty_questions}")
    print(f"Questions without answers: {questions_without_answers}")
    print(f"Answers without text   : {answers_without_text}")
    print(f"Duplicate question IDs : {duplicate_ids}")

    total_issues = (
        empty_documents
        + empty_paragraphs
        + empty_questions
        + questions_without_answers
        + answers_without_text
        + duplicate_ids
    )

    print("\n" + "=" * 35)

    if total_issues == 0:
        print("RESULT: No obvious data quality issues found.")
    else:
        print(f"RESULT: {total_issues} potential issue(s) found.")


if __name__ == "__main__":
    dataset_path = input("Enter CUAD JSON file path: ").strip()
    generate_quality_report(dataset_path)