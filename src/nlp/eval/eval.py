from __future__ import annotations

from typing import Dict, List

from .metrics import compute_metrics


def evaluate(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    """Run evaluation for the model."""
    return compute_metrics(y_true, y_pred)
