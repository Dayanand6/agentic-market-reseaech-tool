from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://agentic-market-reseaech-tool-dqchpsrmeccxqf93gcayg7.streamlit.app"
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
agent = ResearchAgent()

# Rate limiting is applied per client IP address.
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


@app.get("/")
def root():
    return {"message": "Agentic Market Research Tool API is running"}


@app.post("/research", response_model=ResearchResponse)
@limiter.limit("5/minute")
def research(
    request: Request,
    payload: ResearchRequest,
    db: Session = Depends(get_db)
):
    try:
        result = agent.run(payload.query)

        if result["status"] == "no_data":
            return {
                "query": result["query"],
                "status": result["status"],
                "message": result["message"],
                "summary": result["summary"],
                "results": result["results"],
                "report": None
            }

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

    except Exception as e:
        # Full details stay server-side.
        print(
            f"Research pipeline failed for query "
            f"'{payload.query}': {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Research pipeline failed. Please try again."
        )


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
        raise HTTPException(
            status_code=404,
            detail="Research record not found"
        )

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
