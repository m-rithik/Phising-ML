from src.nlp.preprocess.normalize import normalize_text


def test_normalize_text_whitespace():
    assert normalize_text("  a   b  ") == "a b"
