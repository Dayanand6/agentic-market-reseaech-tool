from backend.search import SearchEngine


class ResearchAgent:
    def __init__(self):
        self.search_engine = SearchEngine()

    def run(self, query: str) -> dict:
        results = self.search_engine.search(query)

        return {
            "query": query,
            "status": "completed",
            "message": f"Found {len(results)} research result(s)",
            "results": results
        }
