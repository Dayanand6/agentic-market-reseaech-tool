from fastapi import FastAPI
from backend.models import ResearchRequest, ResearchResponse
from backend.agent import ResearchAgent

app = FastAPI(title="Agentic Market Research Tool")

agent = ResearchAgent()


@app.get("/")
def root():
    return {"message": "Agentic Market Research Tool API is running"}


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    result = agent.run(request.query)

    return {
        "query": result["query"],
        "status": result["status"],
        "message": result["message"],
        "summary": result["summary"],
        "results": result["results"]
    }
