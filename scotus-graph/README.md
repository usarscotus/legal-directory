# SCOTUS Graph

Utilities for building a dataset of Supreme Court opinions and citations.

## Ingest scripts
- `scripts/ingest/courtlistener.py` – pull opinions from CourtListener and
  store raw JSON/text plus a normalized table.
- `scripts/ingest/scdb.py` – download SCDB CSVs, extract topic metadata, and
  match to CourtListener opinions by docket or citation.

Raw files are written to `data/raw/` and processed tables to `data/processed/`.
