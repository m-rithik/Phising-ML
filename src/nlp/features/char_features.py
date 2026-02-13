from __future__ import annotations

from typing import Dict


def extract_char_features(text: str) -> Dict[str, float]:
    """Extract character-level features like punctuation density."""
    if not text:
        return {"length": 0.0, "punct_density": 0.0}
    punct = sum(1 for c in text if not c.isalnum() and not c.isspace())
    return {
        "length": float(len(text)),
        "punct_density": float(punct) / max(1.0, float(len(text))),
    }
