"""Ingest SCOTUS opinions from CourtListener.

This script queries the CourtListener REST API for Supreme Court opinions,
downloads the full opinion text, collects citation metadata, and stores the
raw and processed data on disk.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from typing import Iterable, List, Dict, Any
from urllib.parse import urlencode
from urllib.request import urlopen

BASE_URL = "https://www.courtlistener.com/api/rest/v3/opinions/"
RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "courtlistener"
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"


def fetch_json(url: str) -> Dict[str, Any]:
    """Retrieve JSON content from *url*."""
    with urlopen(url) as resp:  # nosec - simple GET request
        return json.load(resp)


def fetch_text(url: str) -> str:
    """Retrieve plain text from *url*; return empty string on failure."""
    try:
        with urlopen(url) as resp:  # nosec
            return resp.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def pull_opinions(start_date: str, max_cases: int | None = None) -> List[Dict[str, Any]]:
    """Fetch opinions from CourtListener.

    Parameters
    ----------
    start_date:
        Minimum filing date (YYYY-MM-DD).
    max_cases:
        Optional cap on number of opinions to retrieve.
    """
    params = {
        "court": "scotus",
        "date_filed_min": start_date,
        "order_by": "date_filed",
    }
    opinions: List[Dict[str, Any]] = []
    next_url = f"{BASE_URL}?{urlencode(params)}"
    while next_url and (max_cases is None or len(opinions) < max_cases):
        data = fetch_json(next_url)
        for result in data.get("results", []):
            opinions.append(result)
            if max_cases and len(opinions) >= max_cases:
                break
        next_url = data.get("next")
    return opinions


def store_raw(opinion: Dict[str, Any]) -> None:
    """Persist raw JSON and opinion text for *opinion*."""
    opinion_id = opinion["id"]
    json_path = RAW_DIR / f"opinion_{opinion_id}.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(opinion, f)
    text_url = opinion.get("plain_text")
    if text_url:
        text = fetch_text(text_url)
        text_path = RAW_DIR / f"opinion_{opinion_id}.txt"
        with text_path.open("w", encoding="utf-8") as f:
            f.write(text)


def normalize(opinion: Dict[str, Any]) -> Dict[str, Any]:
    """Extract a subset of fields for tabular storage."""
    primary_cite = ""
    for cite in opinion.get("citations", []):
        if cite.get("type") == "official":
            primary_cite = cite.get("cite", "")
            break
    return {
        "id": opinion.get("id"),
        "docket": opinion.get("docket"),
        "case_name": opinion.get("case_name"),
        "date_filed": opinion.get("date_filed"),
        "citation": primary_cite,
        "absolute_url": opinion.get("absolute_url"),
    }


def write_csv(rows: Iterable[Dict[str, Any]], path: Path) -> None:
    """Write *rows* to *path* as CSV."""
    rows = list(rows)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-date", default="1900-01-01", help="Earliest filing date")
    parser.add_argument("--max", type=int, default=None, help="Maximum number of opinions")
    args = parser.parse_args()

    ensure_dirs()
    opinions = pull_opinions(args.start_date, args.max)
    for opinion in opinions:
        store_raw(opinion)
    normalized = [normalize(o) for o in opinions]
    write_csv(normalized, PROCESSED_DIR / "courtlistener_opinions.csv")


if __name__ == "__main__":
    main()
