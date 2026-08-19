import re


def normalize_text(text):
    """
    Normalize contract text for NLP preprocessing.

    Steps:
    1. Convert text to lowercase.
    2. Replace newlines and tabs with spaces.
    3. Remove extra whitespace.
    4. Remove unnecessary punctuation.
    """

    if not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Replace newlines and tabs with spaces
    text = re.sub(r"[\r\n\t]+", " ", text)

    # Remove unnecessary punctuation but preserve
    # characters commonly useful in contract text.
    text = re.sub(r"[^\w\s.,;:()/%$-]", "", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


if __name__ == "__main__":
    sample_text = """
    THIS AGREEMENT is entered into by the PARTIES.
    The payment shall be $10,000.00 per month.
    """

    normalized = normalize_text(sample_text)

    print("Original Text:")
    print(sample_text)

    print("\nNormalized Text:")
    print(normalized)