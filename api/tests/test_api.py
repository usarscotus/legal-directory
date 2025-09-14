import datetime
import os
import sys

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure the package root is on the import path when tests are executed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from api.main import app
from api import database, graph, search


# Setup file-based database and populate with a sample case
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database.engine = engine
database.SessionLocal = TestingSessionLocal
database.Base.metadata.create_all(bind=engine)

session = TestingSessionLocal()
session.add(database.Case(id=1, title="Test Case", text="Lorem ipsum", topic="civil", date=datetime.date(2020, 1, 1)))
session.commit()
session.close()

# Populate citation graph
graph.citation_graph.graph.clear()
graph.citation_graph.add_case(1)
graph.citation_graph.add_case(2)
graph.citation_graph.add_citation(2, 1)

# Stub search service

def fake_search_cases(query, topic=None, date=None):
    return [
        {
            "id": 1,
            "title": "Test Case",
            "text": "Lorem ipsum",
            "topic": "civil",
            "date": datetime.date(2020, 1, 1),
        }
    ]


search.search_cases = fake_search_cases

client = TestClient(app)


def test_get_case():
    response = client.get("/cases/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Case"


def test_get_citations():
    response = client.get("/cases/1/citations")
    assert response.status_code == 200
    assert response.json() == {"incoming": [2], "outgoing": []}


def test_search():
    response = client.get("/search", params={"q": "test"})
    assert response.status_code == 200
    body = response.json()
    assert body[0]["id"] == 1
