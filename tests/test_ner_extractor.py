from backend.app.nlp.ner_extractor import extract_entities


def test_extract_contract_entities():
    text = """
    Microsoft Corporation will pay USD 50,000 on January 15, 2027
    in New York.
    """

    entities = extract_entities(text)

    assert isinstance(entities, list)

    labels = {entity["label"] for entity in entities}

    assert "ORG" in labels
    assert "MONEY" in labels
    assert "DATE" in labels
    assert "GPE" in labels


def test_empty_contract_text():
    assert extract_entities("") == []