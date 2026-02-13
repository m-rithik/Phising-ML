from __future__ import annotations

import re
from typing import Dict

_URL_RE = re.compile(r"https?://\S+|www\.\S+")


def extract_url_features(text: str) -> Dict[str, float]:
    """Extract URL-based features."""
    urls = _URL_RE.findall(text or "")
    return {
        "url_count": float(len(urls)),
        "has_url": float(bool(urls)),
    }
