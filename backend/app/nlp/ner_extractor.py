"""
Baseline Named Entity Recognition for contract documents.

Uses spaCy's pretrained English NER model and lightweight
pattern matching for common legal contract entities.
"""

import re
from typing import Any

import spacy


try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None


def extract_entities(text: str) -> list[dict[str, Any]]:
    """Extract organizations, dates, money, parties, and jurisdictions."""
    if not isinstance(text, str) or not text.strip():
        return []

    entities: list[dict[str, Any]] = []

    if nlp is not None:
        doc = nlp(text)

        for ent in doc.ents:
            if ent.label_ in {"ORG", "DATE", "MONEY", "GPE", "LOC"}:
                entities.append(
                    {
                        "text": ent.text,
                        "label": ent.label_,
                        "start": ent.start_char,
                        "end": ent.end_char,
                    }
                )

    # Detect common monetary values that spaCy may miss.
    money_pattern = r"(?:USD|EUR|GBP|INR|\$|€|£|₹)\s?\d[\d,]*(?:\.\d+)?"

    existing_money = {
        entity["text"] for entity in entities if entity["label"] == "MONEY"
    }

    for match in re.finditer(money_pattern, text, re.IGNORECASE):
        if match.group() not in existing_money:
            entities.append(
                {
                    "text": match.group(),
                    "label": "MONEY",
                    "start": match.start(),
                    "end": match.end(),
                }
            )

    return sorted(entities, key=lambda entity: entity["start"])