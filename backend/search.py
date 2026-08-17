class SearchEngine:
    def search(self, query: str) -> list:
        return [
            {
                "title": f"Search result for: {query}",
                "snippet": "Placeholder search result"
            }
        ]
