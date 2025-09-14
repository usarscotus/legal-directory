"""FastAPI service exposing case data and search."""

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Iterable, List

from . import database, graph, schemas, search

app = FastAPI(title="Legal Directory API")
router = APIRouter()


@router.get("/cases/{case_id}", response_model=schemas.Case)
def read_case(case_id: int, db: Session = Depends(database.get_db)):
    case = database.get_case(db, case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.get("/cases/{case_id}/citations", response_model=schemas.CitationResponse)
def read_citations(case_id: int):
    return graph.citation_graph.citations_for(case_id)


@router.get("/search", response_model=List[schemas.Case])
def search_endpoint(
    q: str | None = None,
    category: str | None = None,
    term: str | None = None,
    year: int | None = None,
    litigant: str | None = None,
    keywords: Iterable[str] | None = Query(default=None),
):
    results = search.search_cases(
        query=q,
        category=category,
        term=term,
        year=year,
        litigant=litigant,
        keywords=keywords,
    )
    return [schemas.Case(**r) for r in results]


app.include_router(router, prefix="/api")
