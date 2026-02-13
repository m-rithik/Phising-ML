from __future__ import annotations

import argparse

from src.nlp.training.train import train_model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    # TODO: load config
    train_model({"config": args.config})


if __name__ == "__main__":
    main()
