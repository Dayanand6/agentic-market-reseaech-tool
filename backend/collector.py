import trafilatura


def fetch_full_content(url: str, max_chars: int = 8000) -> str | None:
    """
    Download a webpage and extract clean article text.

    Returns None if the fetch or extraction fails.
    """
    try:
        downloaded = trafilatura.fetch_url(url)

        if downloaded is None:
            return None

        text = trafilatura.extract(downloaded)

        if text is None or len(text.strip()) < 200:
            return None

        return text[:max_chars]

    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def collect_data(sources: list[dict]) -> list[dict]:
    """
    Enrich search results with full webpage content.

    If full extraction fails, keep the original Tavily
    snippet so the source is not lost.
    """
    enriched = []

    for source in sources:
        full_text = fetch_full_content(source["url"])

        enriched.append({
            "title": source["title"],
            "url": source["url"],
            "content": full_text if full_text else source["snippet"]
        })

    return enriched
