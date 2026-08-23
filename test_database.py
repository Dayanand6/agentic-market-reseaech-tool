from backend.database import (
    init_db,
    SessionLocal,
    save_research_run,
    get_all_records
)


init_db()

db = SessionLocal()

fake_sources = [
    {
        "title": "Test Article",
        "url": "https://example.com",
        "content": "Some content here"
    }
]

fake_report = {
    "market_overview": "Test overview",
    "key_trends": ["Trend 1", "Trend 2"],
    "competitor_landscape": "Test competitors",
    "consumer_sentiment": "Test sentiment",
    "risks_opportunities": "Test risks",
    "sources_referenced": ["https://example.com"]
}

record = save_research_run(
    db,
    "test query",
    fake_sources,
    fake_report
)

print(f"Saved record #{record.id}")

all_records = get_all_records(db)

for r in all_records:
    print(f"#{r.id} - {r.query} - {r.created_at}")

db.close()
