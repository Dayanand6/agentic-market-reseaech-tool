from fastapi import FastAPI
from backend.models import ResearchRequest,ResearchResponse

app = FastAPI(title="Agentic Market Research Tool")


@app.get("/")
def root():
    return {"message": "Agentic Market Research Tool API is running"}


@app.post("/research",
response_model=ResearchResponse)
def research(request: ResearchRequest):
    return {
        "query": request.query,
        "message": "Research request received"
    }
