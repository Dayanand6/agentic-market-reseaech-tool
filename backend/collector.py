import trafilatura


SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "disregard the above",
    "disregard previous",
    "new instructions:",
    "system prompt",
    "you are now",
]


def flag_suspicious_content(text: str) -> bool:
    """
    Basic heuristic check for text resembling a prompt injection attempt.

    This is a monitoring layer, not a blocking mechanism.
    """
    lowered = text.lower()

    return any(
        pattern in lowered
        for pattern in SUSPICIOUS_PATTERNS
    )


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

        content = full_text if full_text else source["snippet"]

        if flag_suspicious_content(content):
            print(
                f"⚠️ Suspicious content pattern detected in: "
                f"{source['url']}"
            )

        enriched.append({
            "title": source["title"],
            "url": source["url"],
            "content": content
        })

    return enriched
