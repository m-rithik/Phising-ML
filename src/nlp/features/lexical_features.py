from __future__ import annotations

from typing import Dict

# Placeholder lexical cues (to be replaced by learned lists)
_SUSPICIOUS_CUES = [
    "otp",
    "password",
    "kyc",
    "verify",
    "urgent",
    "account",
]


def extract_lexical_features(text: str) -> Dict[str, float]:
    """Extract simple lexical cues."""
    text_l = (text or "").lower()
    score = sum(1 for cue in _SUSPICIOUS_CUES if cue in text_l)
    return {
        "lexical_cue_count": float(score),
        "has_lexical_cue": float(score > 0),
    }
