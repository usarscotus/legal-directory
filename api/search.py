"""Elasticsearch integration for case search."""

import os
from typing import Any, Dict, List
from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
es_client = Elasticsearch(ELASTICSEARCH_URL)


def search_cases(query: str, topic: str | None = None, date: str | None = None) -> List[Dict[str, Any]]:
    """Search cases using Elasticsearch with optional filters."""
    must: List[Dict[str, Any]] = [{"multi_match": {"query": query, "fields": ["title", "text"]}}]
    filters: List[Dict[str, Any]] = []
    if topic:
        filters.append({"term": {"topic": topic}})
    if date:
        filters.append({"term": {"date": date}})

    body = {"query": {"bool": {"must": must, "filter": filters}}}
    response = es_client.search(index="cases", body=body)
    return [hit["_source"] for hit in response["hits"]["hits"]]
