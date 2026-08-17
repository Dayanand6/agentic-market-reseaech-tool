class ResearchReporter:

    def generate(self, query: str, results: list[dict]) -> dict:
        return {
            "query": query,
            "summary": f"Research collected {len(results)} sources for: {query}",
            "sources": results
        }
