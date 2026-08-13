from fastapi import FastAPI
from backend.models import ResearchRequest

app = FastAPI(title="Agentic Market Research Tool")


@app.get("/")
def root():
    return {"message": "Agentic Market Research Tool API is running"}


@app.post("/research")
def research(request: ResearchRequest):
    return {
        "query": request.query,
        "message": "Research request received"
    }
