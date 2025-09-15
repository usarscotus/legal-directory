"""Elasticsearch integration for case search."""

import os
from typing import Any, Dict, Iterable, List

from elasticsearch import Elasticsearch, NotFoundError

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
es_client = Elasticsearch(ELASTICSEARCH_URL)


def _append_filter(filters: List[Dict[str, Any]], field: str, value: Any) -> None:
    """Helper to append an Elasticsearch term filter when a value is provided."""
    if value is not None:
        filters.append({"term": {field: value}})


def search_cases(
    query: str | None = None,
    *,
    category: str | None = None,
    term: str | None = None,
    year: int | None = None,
    litigant: str | None = None,
    keywords: Iterable[str] | None = None,
) -> List[Dict[str, Any]]:
    """Search cases using Elasticsearch with rich filtering options.

    By default only cases with ``status`` of ``decided`` are returned.
    """

    must: List[Dict[str, Any]] = []
    if query:
        must.append({"multi_match": {"query": query, "fields": ["title", "text", "keywords"]}})
    if keywords:
        must.append({"terms": {"keywords": list(keywords)}})
    if not must:
        must.append({"match_all": {}})

    filters: List[Dict[str, Any]] = []
    # Always exclude undecided cases
    _append_filter(filters, "status", "decided")
    _append_filter(filters, "topic", category)
    _append_filter(filters, "term", term)
    _append_filter(filters, "year", year)
    if litigant:
        filters.append({"match": {"litigants": litigant}})

    body = {"query": {"bool": {"must": must, "filter": filters}}}
    response = es_client.search(index="cases", body=body)
    return [{"id": int(hit["_id"]), **hit["_source"]} for hit in response["hits"]["hits"]]


def get_case(case_id: int) -> Dict[str, Any] | None:
    """Return metadata for a single case by ID.

    The relational database stores core fields while Elasticsearch keeps
    enhanced metadata like votes, opinions, and citation relationships. This
    helper fetches the latter so API endpoints can present a unified view.
    """

    try:
        doc = es_client.get(index="cases", id=case_id)
    except NotFoundError:
        return None
    return {"id": int(doc["_id"]), **doc["_source"]}
