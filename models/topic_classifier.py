"""Topic classification for Supreme Court Database (SCDB) issues."""

from __future__ import annotations

from typing import List

from transformers import pipeline

SCDB_TOPICS: List[str] = [
    "Criminal Procedure",
    "Civil Rights",
    "First Amendment",
    "Due Process",
    "Privacy",
    "Attorneys",
    "Unions",
    "Economic Activity",
    "Judicial Power",
    "Federalism",
    "Interstate Relations",
    "Federal Taxation",
    "Miscellaneous",
    "Unspecified",
]


class TopicClassifier:
    """Predict the best matching SCDB topic for a piece of text."""

    def __init__(self, model_name: str = "valhalla/distilbart-mnli-12-6") -> None:
        self._classifier = pipeline("zero-shot-classification", model=model_name)

    def predict(self, text: str) -> str:
        """Return the highest-scoring SCDB topic for *text*."""
        result = self._classifier(text, SCDB_TOPICS)
        return result["labels"][0]
