"""FastAPI service exposing case data and search."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import database, graph, schemas, search

app = FastAPI(title="Legal Directory API")


@app.get("/cases/{case_id}", response_model=schemas.Case)
def read_case(case_id: int, db: Session = Depends(database.get_db)):
    case = database.get_case(db, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@app.get("/cases/{case_id}/citations", response_model=schemas.CitationResponse)
def read_citations(case_id: int):
    return graph.citation_graph.citations_for(case_id)


@app.get("/search", response_model=List[schemas.Case])
def search_endpoint(q: str, topic: str | None = None, date: str | None = None):
    results = search.search_cases(q, topic=topic, date=date)
    return [schemas.Case(**r) for r in results]
