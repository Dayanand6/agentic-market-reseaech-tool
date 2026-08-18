from backend.search import run_searches


results = run_searches([
    "EV market size India 2026",
    "top electric vehicle companies India"
])


for result in results:
    print(result["title"], "-", result["url"])
