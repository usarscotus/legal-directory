-- SQL schema for SCOTUS graph data

-- Table of Supreme Court opinions from CourtListener
CREATE TABLE IF NOT EXISTS opinions (
    id INTEGER PRIMARY KEY,
    docket TEXT,
    case_name TEXT,
    date_filed DATE,
    citation TEXT,
    absolute_url TEXT
);

-- Table capturing citation relationships between opinions
CREATE TABLE IF NOT EXISTS citations (
    source_id INTEGER NOT NULL REFERENCES opinions(id),
    target_id INTEGER NOT NULL REFERENCES opinions(id)
);
