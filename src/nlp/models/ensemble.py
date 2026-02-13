from __future__ import annotations

from typing import Dict, List


def ensemble_scores(semantic: List[float], char: List[float], features: List[Dict[str, float]]) -> List[float]:
    """Combine model scores and features into a single risk score.

    Placeholder weighting logic.
    """
    scores = []
    for i in range(len(semantic)):
        feat_bonus = 0.01 * sum(features[i].values()) if i < len(features) else 0.0
        scores.append(0.6 * semantic[i] + 0.3 * char[i] + feat_bonus)
    return scores
