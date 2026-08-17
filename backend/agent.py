from backend.search import SearchEngine
from backend.reporter import ResearchReporter


class ResearchAgent:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.reporter = ResearchReporter()

    def run(self, query: str) -> dict:
        results = self.search_engine.search(query)
        report = self.reporter.generate(query, results)

        return {
            "query": query,
            "status": "completed",
            "message": f"Found {len(results)} research result(s)",
            "results": results,
            "summary": report["summary"]
        }
