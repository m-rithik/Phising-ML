from __future__ import annotations

from typing import List


class SemanticEncoder:
    """Placeholder wrapper for a multilingual transformer encoder."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def encode(self, texts: List[str]) -> List[List[float]]:
        # TODO: integrate actual model
        return [[0.0] * 8 for _ in texts]
