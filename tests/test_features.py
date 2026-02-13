from src.nlp.features.url_features import extract_url_features
from src.nlp.features.lexical_features import extract_lexical_features


def test_url_features():
    feats = extract_url_features("visit https://example.com")
    assert feats["url_count"] == 1.0


def test_lexical_features():
    feats = extract_lexical_features("Please verify OTP")
    assert feats["has_lexical_cue"] == 1.0
