from __future__ import annotations

from typing import List


class CharModel:
    """Placeholder wrapper for a character-level model."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def score(self, texts: List[str]) -> List[float]:
        # TODO: integrate actual model
        return [0.0 for _ in texts]
