from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Sample:
    text: str
    label: int
    language: str
    script: str


def load_samples(path: str) -> List[Sample]:
    """Load samples from a JSONL dataset."""
    # TODO: implement JSONL loader
    return []
