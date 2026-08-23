import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Agentic Market Research Tool",
    layout="wide",
)

st.title("🔍 Agentic Market Research Tool")

# --- Sidebar: past research history ---
st.sidebar.header("Past Research")

try:
    history = requests.get(
        f"{BACKEND_URL}/research/history",
        timeout=5,
    ).json()
except requests.exceptions.RequestException:
    history = []
    st.sidebar.error(
        "Backend not reachable. Is it running?\n\n"
        "`uvicorn backend.main:app --reload`"
    )

for item in history:
    if st.sidebar.button(
        item["query"],
        key=f"history_{item['id']}",
    ):
        past = requests.get(
            f"{BACKEND_URL}/research/{item['id']}"
        ).json()

        st.session_state["active_report"] = {
            "query": past["query"],
            "report": past["report"],
        }

# --- Main: new research input ---
query = st.text_input(
    "What market do you want to research?",
    placeholder="e.g. EV market in India",
)

if st.button("Run Research", type="primary") and query:
    with st.spinner(
        "Running research pipeline — this can take 30–60 seconds..."
    ):
        try:
            response = requests.post(
                f"{BACKEND_URL}/research",
                json={"query": query},
                timeout=180,
            )
            response.raise_for_status()
            result = response.json()

            st.session_state["active_report"] = {
                "query": result["query"],
                "report": result["report"],
            }

        except requests.exceptions.RequestException as e:
            st.error(f"Research failed: {e}")

# --- Display whichever report is active ---
if "active_report" in st.session_state:
    active = st.session_state["active_report"]
    report = active["report"]

    st.header(f"Report: {active['query']}")

    st.subheader("📊 Market Overview")
    st.write(report["market_overview"])

    st.subheader("📈 Key Trends")
    for trend in report["key_trends"]:
        st.markdown(f"- {trend}")

    st.subheader("🏢 Competitor Landscape")
    st.write(report["competitor_landscape"])

    st.subheader("💬 Consumer Sentiment")
    st.write(report["consumer_sentiment"])

    st.subheader("⚠️ Risks & Opportunities")
    st.write(report["risks_opportunities"])

    st.subheader("🔗 Sources Referenced")
    for url in report["sources_referenced"]:
        st.markdown(f"- {url}")
else:
    st.info("Enter a query above and click 'Run Research' to get started.")
