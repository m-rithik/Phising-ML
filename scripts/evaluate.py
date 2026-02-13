from __future__ import annotations

import argparse

from src.nlp.eval.eval import evaluate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred", required=True)
    parser.add_argument("--gold", required=True)
    args = parser.parse_args()
    # TODO: load predictions
    metrics = evaluate([], [])
    print(metrics)


if __name__ == "__main__":
    main()
