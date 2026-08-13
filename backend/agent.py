class ResearchAgent:
    def run(self, query: str) -> dict:
        return {
            "query": query,
            "status": "received",
            "message": "Research agent received the query"
        }
