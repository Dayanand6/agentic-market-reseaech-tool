from backend.agent import create_research_plan
from backend.search import SearchEngine
from backend.collector import collect_data
from backend.analyzer import analyze_market_research


query = "EV market in India"

print("Creating research plan...")
search_queries = create_research_plan(query)

print("\nPlanned searches:")
for q in search_queries:
    print("-", q)

print("\nExecuting searches...")

search_engine = SearchEngine()
all_results = []

for search_query in search_queries:
    results = search_engine.search(search_query)
    all_results.extend(results)

print(f"Collected {len(all_results)} search results")

print("\nCollecting full webpage content...")
enriched_results = collect_data(all_results)

print(f"Enriched {len(enriched_results)} sources")

print("\nAnalyzing market research...")
report = analyze_market_research(
    query,
    enriched_results
)

print("\n--- MARKET OVERVIEW ---")
print(report["market_overview"])

print("\n--- KEY TRENDS ---")
for trend in report["key_trends"]:
    print("-", trend)

print("\n--- COMPETITOR LANDSCAPE ---")
print(report["competitor_landscape"])

print("\n--- CONSUMER SENTIMENT ---")
print(report["consumer_sentiment"])

print("\n--- RISKS / OPPORTUNITIES ---")
print(report["risks_opportunities"])

print("\n--- SOURCES REFERENCED ---")
for url in report["sources_referenced"]:
    print("-", url)
