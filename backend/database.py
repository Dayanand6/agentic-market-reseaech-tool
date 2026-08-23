from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker
)


# SQLite database file
DATABASE_URL = "sqlite:///./research.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class ResearchRecord(Base):
    __tablename__ = "research_records"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(300), nullable=False)
    status = Column(String(50), default="complete")
    created_at = Column(DateTime, default=datetime.utcnow)

    # One record has many sources, and exactly one report
    sources = relationship(
        "Source",
        back_populates="record",
        cascade="all, delete-orphan"
    )

    report = relationship(
        "Report",
        back_populates="record",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(
        Integer,
        ForeignKey("research_records.id"),
        nullable=False
    )
    title = Column(String(500))
    url = Column(String(1000))
    content = Column(Text)

    record = relationship(
        "ResearchRecord",
        back_populates="sources"
    )


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(
        Integer,
        ForeignKey("research_records.id"),
        unique=True,
        nullable=False
    )

    market_overview = Column(Text)
    key_trends = Column(JSON)
    competitor_landscape = Column(Text)
    consumer_sentiment = Column(Text)
    risks_opportunities = Column(Text)
    sources_referenced = Column(JSON)

    record = relationship(
        "ResearchRecord",
        back_populates="report"
    )


def init_db():
    """Creates all tables if they don't already exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    FastAPI will call this for every request that needs
    the database, then close the session automatically.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def save_research_run(
    db,
    query: str,
    sources: list[dict],
    report: dict
) -> ResearchRecord:
    """
    Saves a completed research run: the original query,
    every source, and the final report.
    """

    record = ResearchRecord(
        query=query,
        status="complete"
    )

    db.add(record)

    # Assign record.id without committing yet
    db.flush()

    for source in sources:
        db.add(
            Source(
                record_id=record.id,
                title=source["title"],
                url=source["url"],
                content=source["content"]
            )
        )

    db.add(
        Report(
            record_id=record.id,
            market_overview=report["market_overview"],
            key_trends=report["key_trends"],
            competitor_landscape=report["competitor_landscape"],
            consumer_sentiment=report["consumer_sentiment"],
            risks_opportunities=report["risks_opportunities"],
            sources_referenced=report["sources_referenced"]
        )
    )

    db.commit()
    db.refresh(record)

    return record


def get_all_records(db):
    """Returns every past research run, newest first."""

    return (
        db.query(ResearchRecord)
        .order_by(ResearchRecord.created_at.desc())
        .all()
    )


def get_record_by_id(db, record_id: int):
    """Returns one specific past research run, or None."""

    return (
        db.query(ResearchRecord)
        .filter(ResearchRecord.id == record_id)
        .first()
    )
