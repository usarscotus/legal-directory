"""Relational database integration using SQLAlchemy."""

import os
from sqlalchemy import Column, Date, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cases.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(Text)
    topic = Column(String, index=True)
    date = Column(Date, index=True)


def get_case(db: Session, case_id: int) -> Case | None:
    return db.get(Case, case_id)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
