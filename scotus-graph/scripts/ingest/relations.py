"""Extract citation relationships from CourtListener opinions.

This script reads previously downloaded opinion JSON files from CourtListener
and derives citation edges between opinions. The resulting pairs are written to
`data/processed/courtlistener_citations.csv` with columns:

- ``source_id`` – the citing opinion's CourtListener identifier
- ``target_id`` – the cited opinion's CourtListener identifier
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "courtlistener"
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

# Pattern to extract opinion ID from CourtListener URLs
ID_RE = re.compile(r"/opinion/(\d+)/")


def extract_edges(opinion: Dict) -> List[Dict[str, int]]:
    """Return citation edges for a single *opinion* object."""
    src = opinion.get("id")
    edges: List[Dict[str, int]] = []
    for url in opinion.get("cites_to", []) or []:
        match = ID_RE.search(url)
        if match and src is not None:
            edges.append({"source_id": int(src), "target_id": int(match.group(1))})
    return edges


def gather_edges(paths: Iterable[Path]) -> List[Dict[str, int]]:
    """Collect citation edges from iterable of JSON *paths*."""
    all_edges: List[Dict[str, int]] = []
    for path in paths:
        try:
            opinion = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        all_edges.extend(extract_edges(opinion))
    return all_edges


def write_csv(rows: Iterable[Dict[str, int]], path: Path) -> None:
    rows = list(rows)
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source_id", "target_id"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default=PROCESSED_DIR / "courtlistener_citations.csv",
        type=Path,
        help="Output CSV path",
    )
    args = parser.parse_args()

    json_files = RAW_DIR.glob("opinion_*.json")
    edges = gather_edges(json_files)
    write_csv(edges, args.out)


if __name__ == "__main__":
    main()
