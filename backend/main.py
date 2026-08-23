from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend.models import ResearchRequest, ResearchResponse
from backend.agent import ResearchAgent
from backend.database import (
    init_db,
    get_db,
    save_research_run,
    get_all_records,
    get_record_by_id
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Agentic Market Research Tool",
    lifespan=lifespan
)

agent = ResearchAgent()


@app.get("/")
def root():
    return {"message": "Agentic Market Research Tool API is running"}


@app.post("/research", response_model=ResearchResponse)
def research(
    request: ResearchRequest,
    db: Session = Depends(get_db)
):
    result = agent.run(request.query)

    save_research_run(
        db,
        result["query"],
        result["results"],
        result["report"]
    )

    return {
        "query": result["query"],
        "status": result["status"],
        "message": result["message"],
        "summary": result["summary"],
        "results": result["results"],
        "report": result["report"]
    }


@app.get("/research/history")
def research_history(db: Session = Depends(get_db)):
    records = get_all_records(db)

    return [
        {
            "id": r.id,
            "query": r.query,
            "created_at": r.created_at
        }
        for r in records
    ]


@app.get("/research/{record_id}")
def get_past_research(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = get_record_by_id(db, record_id)

    if not record:
        return {"error": "Research record not found"}

    return {
        "id": record.id,
        "query": record.query,
        "created_at": record.created_at,
        "report": {
            "market_overview": record.report.market_overview,
            "key_trends": record.report.key_trends,
            "competitor_landscape": record.report.competitor_landscape,
            "consumer_sentiment": record.report.consumer_sentiment,
            "risks_opportunities": record.report.risks_opportunities,
            "sources_referenced": record.report.sources_referenced
        },
        "sources": [
            {
                "title": s.title,
                "url": s.url
            }
            for s in record.sources
        ]
    }
