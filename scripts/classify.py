#!/usr/bin/env python3
"""Classify opinions into SCDB topics using a transformer model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from models import TopicClassifier


def iter_opinion_files(directory: Path):
    for path in sorted(directory.glob("*.json")):
        if path.is_file():
            yield path


def classify_files(directory: Path, classifier: TopicClassifier) -> None:
    for path in iter_opinion_files(directory):
        with path.open() as f:
            data = json.load(f)
        text = data.get("text") or data.get("content") or ""
        if not text:
            continue
        topic = classifier.predict(text)
        data["predicted_topic"] = topic
        with path.open("w") as f:
            json.dump(data, f, indent=2)
        print(f"{path.name}: {topic}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "processed",
        help="Directory containing opinion JSON files",
    )
    parser.add_argument(
        "--model",
        default="valhalla/distilbart-mnli-12-6",
        help="Hugging Face model name for zero-shot classification",
    )
    args = parser.parse_args()

    classifier = TopicClassifier(args.model)
    classify_files(args.data_dir, classifier)


if __name__ == "__main__":
    main()
