from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class LanguageSegment:
    text: str
    language: str
    script: str
    start: int
    end: int


def detect_language_segments(text: str) -> List[LanguageSegment]:
    """Detect language and script segments within a message.

    Placeholder implementation. Replace with a model-backed segmenter.
    """
    if not text:
        return []
    return [LanguageSegment(text=text, language="unknown", script="unknown", start=0, end=len(text))]
