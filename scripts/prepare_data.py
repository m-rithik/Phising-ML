from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    # TODO: implement data preparation
    print(f"Preparing data from {args.input} -> {args.output}")


if __name__ == "__main__":
    main()
