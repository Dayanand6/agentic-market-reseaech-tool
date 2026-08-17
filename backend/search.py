from ddgs import DDGS


class SearchEngine:
    def search(self, query: str, max_results: int = 5) -> list:
        results = DDGS().text(
            query,
            region="in-en",
            safesearch="moderate",
            max_results=max_results
        )

        return [
            {
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", "")
            }
            for result in results
        ]
