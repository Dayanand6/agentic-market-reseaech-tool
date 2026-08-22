from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()


# Gemini function/tool definition for market analysis
ANALYSIS_TOOL = {
    "type": "function",
    "name": "create_market_report",
    "description": (
        "Produces a structured market research report using ONLY "
        "the provided source material. Every claim must be traceable "
        "to one of the given sources — do not use outside knowledge."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "market_overview": {
                "type": "string",
                "description": (
                    "2-4 sentence summary of the market's current "
                    "state and size, based only on the sources"
                )
            },
            "key_trends": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": (
                    "3-5 bullet points on major trends found "
                    "in the sources"
                )
            },
            "competitor_landscape": {
                "type": "string",
                "description": (
                    "Summary of key players/competitors "
                    "mentioned in the sources"
                )
            },
            "consumer_sentiment": {
                "type": "string",
                "description": (
                    "Summary of consumer opinion or adoption "
                    "found in the sources; say 'Not enough data "
                    "in sources' if absent"
                )
            },
            "risks_opportunities": {
                "type": "string",
                "description": (
                    "Key risks and opportunities identified "
                    "from the sources"
                )
            },
            "sources_referenced": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": (
                    "URLs of the sources actually used to "
                    "support the claims above"
                )
            }
        },
        "required": [
            "market_overview",
            "key_trends",
            "competitor_landscape",
            "consumer_sentiment",
            "risks_opportunities",
            "sources_referenced"
        ]
    }
}


def build_source_context(sources: list[dict]) -> str:
    """
    Formats collected sources into a numbered block
    the model can read and cite from.
    """

    blocks = []

    for i, source in enumerate(sources, start=1):
        blocks.append(
            f"[Source {i}]\n"
            f"{source['title']}\n"
            f"URL: {source['url']}\n"
            f"{source['content']}"
        )

    return "\n\n---\n\n".join(blocks)


def analyze_market_research(
    user_query: str,
    sources: list[dict]
) -> dict:
    """
    Feeds collected sources to the LLM and returns
    a structured market research report.
    """

    source_context = build_source_context(sources)

    prompt = f"""
You are a market research analyst.

A user asked:
"{user_query}"

Below are {len(sources)} sources gathered from the web.

Use ONLY the information in these sources to build your report.
Do not rely on prior knowledge, and do not invent statistics or
facts that aren't present in the source text below.

If the sources don't cover something, say so explicitly rather
than guessing.

{source_context}
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
        tools=[ANALYSIS_TOOL],
        generation_config={
            "tool_choice": {
                "allowed_tools": {
                    "mode": "any",
                    "tools": ["create_market_report"]
                }
            }
        }
    )

    fc_step = next(
        step
        for step in interaction.steps
        if step.type == "function_call"
    )

    return fc_step.arguments
