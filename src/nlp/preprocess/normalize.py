from __future__ import annotations

import re

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Normalize text for downstream NLP models.

    Steps:
    - Strip leading/trailing whitespace
    - Normalize repeated whitespace
    - Preserve URLs and digits
    """
    if text is None:
        return ""
    text = text.strip()
    text = _WHITESPACE_RE.sub(" ", text)
    return text
