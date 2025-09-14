from __future__ import annotations

import datetime as dt
from pydantic import BaseModel, ConfigDict
from typing import List


class Case(BaseModel):
    """Representation of a legal case."""
    id: int
    title: str
    text: str
    topic: str | None = None
    date: dt.date | None = None
    citation: str | None = None
    vote: str | None = None
    opinions: List[str] | None = None
    cites: List[int] | None = None
    cited_by: List[int] | None = None
    litigants: List[str] | None = None
    term: str | None = None
    year: int | None = None
    category: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CitationResponse(BaseModel):
    """Incoming and outgoing citations for a case."""
    incoming: List[int]
    outgoing: List[int]
