"""Ingest Supreme Court Database (SCDB) metadata and match to CourtListener.

The script downloads an SCDB CSV release, parses topic and issue codes, and
joins the result with previously ingested CourtListener opinions by docket or
citation.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List
from urllib.request import urlopen

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "scdb"
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
COURTLISTENER_CSV = PROCESSED_DIR / "courtlistener_opinions.csv"
DEFAULT_URL = (
    "https://scdb.wustl.edu/_brickFiles/2023/SCDB_2023_01_caseCentered_Citation.csv"
)


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def download_csv(url: str) -> Path:
    """Download SCDB CSV from *url* into RAW_DIR."""
    ensure_dirs()
    filename = url.split("/")[-1]
    path = RAW_DIR / filename
    if not path.exists():
        with urlopen(url) as resp:  # nosec - simple GET request
            path.write_bytes(resp.read())
    return path


def parse_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def load_courtlistener() -> Dict[str, Dict[str, str]]:
    """Load CourtListener opinions keyed by docket and citation."""
    mapping: Dict[str, Dict[str, str]] = {}
    if COURTLISTENER_CSV.exists():
        with COURTLISTENER_CSV.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("docket"):
                    mapping[row["docket"]] = row
                if row.get("citation"):
                    mapping[row["citation"]] = row
    return mapping


def match_cases(scdb_cases: Iterable[Dict[str, str]], cl_map: Dict[str, Dict[str, str]]) -> List[Dict[str, str]]:
    """Attach CourtListener identifiers to SCDB cases."""
    rows: List[Dict[str, str]] = []
    for case in scdb_cases:
        docket = case.get("docketId") or case.get("docket")
        citation = case.get("usCite")
        match = cl_map.get(docket) or cl_map.get(citation) or {}
        row = {
            "caseId": case.get("caseId"),
            "docket": docket,
            "caseName": case.get("caseName"),
            "dateDecision": case.get("dateDecision"),
            "issue": case.get("issue"),
            "issueArea": case.get("issueArea"),
            "cl_id": match.get("id", ""),
        }
        rows.append(row)
    return rows


def write_csv(rows: Iterable[Dict[str, str]], path: Path) -> None:
    rows = list(rows)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="URL of SCDB CSV release")
    args = parser.parse_args()

    path = download_csv(args.url)
    scdb_cases = parse_csv(path)
    cl_map = load_courtlistener()
    matched = match_cases(scdb_cases, cl_map)
    write_csv(matched, PROCESSED_DIR / "scdb_cases.csv")


if __name__ == "__main__":
    main()
