#!/usr/bin/env python3
"""Index case JSON files into Elasticsearch."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from elasticsearch import Elasticsearch


def iter_case_files(directory: Path) -> Iterable[Path]:
    """Yield JSON files from *directory* in sorted order."""
    for path in sorted(directory.glob("*.json")):
        if path.is_file():
            yield path


def load_schema(path: Path) -> dict:
    """Return JSON schema loaded from *path*."""
    with path.open() as f:
        return json.load(f)


def index_cases(es: Elasticsearch, index: str, directory: Path) -> None:
    """Index all case JSON files in *directory* into *index*."""
    for path in iter_case_files(directory):
        with path.open() as f:
            data = json.load(f)

        citation_id = data.get("citation_id") or data.get("id") or data.get("citation")
        if not citation_id:
            continue

        topic_codes = data.get("topic_codes") or data.get("topics") or data.get("predicted_topic") or []
        if isinstance(topic_codes, str):
            topic_codes = [topic_codes]

        doc = {
            "citation_id": citation_id,
            "title": data.get("title"),
            "text": data.get("text") or data.get("content") or "",
            "topic_codes": topic_codes,
            "court": data.get("court"),
            "date": data.get("date") or data.get("decision_date"),
        }

        es.index(index=index, id=citation_id, document=doc)
        print(f"Indexed {citation_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--es-url", default="http://localhost:9200", help="Elasticsearch URL")
    parser.add_argument("--index", default="cases", help="Index name")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "data" / "processed",
        help="Directory containing case JSON files",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "search" / "schema.json",
        help="Path to index schema JSON",
    )
    args = parser.parse_args()

    es = Elasticsearch(args.es_url)

    if not es.indices.exists(index=args.index):
        schema = load_schema(args.schema)
        es.indices.create(index=args.index, body=schema)

    index_cases(es, args.index, args.data_dir)


if __name__ == "__main__":
    main()
