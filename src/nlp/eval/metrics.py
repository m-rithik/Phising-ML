from __future__ import annotations

from typing import Dict, List


def compute_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    """Compute simple precision/recall/F1."""
    if not y_true:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}
