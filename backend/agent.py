from google import genai
from dotenv import load_dotenv

from backend.search import SearchEngine
from backend.reporter import ResearchReporter
from backend.collector import collect_data
from backend.analyzer import analyze_market_research
# Load GEMINI_API_KEY from .env
load_dotenv()

# Create Gemini client
client = genai.Client()


# Gemini function/tool definition
RESEARCH_PLANNER_TOOL = {
    "type": "function",
    "name": "create_research_plan",
    "description": (
        "Breaks a market research query into 3 to 5 specific, "
        "targeted web search queries. Cover market size/trends, "
        "competitor landscape, consumer sentiment, and recent "
        "news where relevant to the query."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "searches": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": (
                    "3 to 5 specific, well-formed "
                    "search engine queries"
                )
            }
        },
        "required": ["searches"]
    }
}


def create_research_plan(user_query: str) -> list[str]:
    """
    Sends the user's query to Gemini and gets back
    a structured list of search queries.
    """

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=(
            f"Create a research plan for this market "
            f"research query: {user_query}"
        ),
        tools=[RESEARCH_PLANNER_TOOL],
        generation_config={
            "tool_choice": {
                "allowed_tools": {
                    "mode": "any",
                    "tools": ["create_research_plan"]
                }
            }
        }
    )

    # Find Gemini's function call
    fc_step = next(
        step
        for step in interaction.steps
        if step.type == "function_call"
    )

    # Gemini returns parsed arguments
    return fc_step.arguments["searches"]


class ResearchAgent:
    """
    Coordinates Gemini planning, web searching,
    and structured reporting.
    """

    def __init__(self):
        self.search_engine = SearchEngine()
        self.reporter = ResearchReporter()

    def run(self, query: str) -> dict:
        # Step 1: Ask Gemini to create a research plan
        search_queries = create_research_plan(query)

        # Step 2: Execute each planned search
        all_results = []

        for search_query in search_queries:
            results = self.search_engine.search(search_query)
            all_results.extend(results)

        # Step 3: Collect full webpage content
        enriched_results = collect_data(all_results)

        # Step 4: Analyze the collected research using Gemini
        analysis = analyze_market_research(
            query,
            enriched_results
        )

        # Step 5: Generate the structured report
        report = self.reporter.generate(query, enriched_results)
        # Step 6: Return the existing response structure
        return {
            "query": query,
            "status": "completed",
            "message": (
                f"Found {len(enriched_results)} research result(s) "
                f"using {len(search_queries)} planned searches"
            ),
            "results": enriched_results,
            "summary": report["summary"],
            "report": analysis
        }
