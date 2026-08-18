import os

from dotenv import load_dotenv
from tavily import TavilyClient


# Load environment variables from .env
load_dotenv()

# Create Tavily client
tavily_client = TavilyClient(
    api_key=os.environ["TAVILY_API_KEY"]
)


def run_searches(
    search_queries: list[str],
    max_results_per_query: int = 4
) -> list[dict]:
    """
    Runs each search query against Tavily.

    Returns a deduplicated list of results containing:
    - title
    - url
    - content snippet
    """

    all_results = []
    seen_urls = set()

    for query in search_queries:

        try:
            response = tavily_client.search(
                query=query,
                max_results=max_results_per_query,
                search_depth="basic"
            )

        except Exception as e:
            # One failed query should not stop
            # the entire research process.
            print(f"Search failed for '{query}': {e}")
            continue

        for result in response.get("results", []):

            url = result.get("url")

            # Skip duplicate URLs
            if url and url not in seen_urls:
                seen_urls.add(url)

                all_results.append({
                    "title": result.get("title", ""),
                    "url": url,
                    "snippet": result.get("content", "")
                })

    return all_results


class SearchEngine:
    """
    SearchEngine compatibility layer used by
    the existing Phase 2 ResearchAgent.
    """

    def search(
        self,
        query: str,
        max_results: int = 4
    ) -> list[dict]:
        return run_searches(
            [query],
            max_results_per_query=max_results
        )
