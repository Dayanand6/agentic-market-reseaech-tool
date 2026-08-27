import html
import streamlit as st
import requests

BACKEND_URL = "https://agentic-market-reseaech-tool-2.onrender.com"

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Agentic Market Research Tool",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>
        /* Main page */
        .main {
            padding-top: 1.5rem;
        }

        /* Header */
        .hero {
            padding: 1.5rem 1.7rem;
            border-radius: 18px;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(120, 120, 120, 0.18);
            background: linear-gradient(
                135deg,
                rgba(49, 51, 63, 0.10),
                rgba(120, 120, 120, 0.04)
            );
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }

        .hero-subtitle {
            font-size: 1rem;
            opacity: 0.72;
            margin-bottom: 0;
        }

        /* Search box */
        .search-card {
            padding: 1.2rem;
            border-radius: 16px;
            border: 1px solid rgba(120, 120, 120, 0.18);
            margin-bottom: 1.25rem;
        }

        /* Metric cards */
        .metric-card {
            padding: 1rem 1.1rem;
            border-radius: 14px;
            border: 1px solid rgba(120, 120, 120, 0.18);
            min-height: 105px;
        }

        .metric-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            opacity: 0.62;
        }

        .metric-value {
            font-size: 1.7rem;
            font-weight: 750;
            margin-top: 0.2rem;
        }

        /* Section cards */
        .section-card {
            padding: 1.2rem 1.3rem;
            border-radius: 16px;
            border: 1px solid rgba(120, 120, 120, 0.18);
            margin-bottom: 1rem;
        }

        .section-title {
            font-size: 1.08rem;
            font-weight: 750;
            margin-bottom: 0.65rem;
        }

        /* Trend cards */
        .trend-item {
            padding: 0.85rem 1rem;
            border-radius: 12px;
            border: 1px solid rgba(120, 120, 120, 0.14);
            margin-bottom: 0.6rem;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(120, 120, 120, 0.15);
        }

        .history-label {
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            opacity: 0.6;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            opacity: 0.55;
            font-size: 0.78rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================

if "active_report" not in st.session_state:
    st.session_state["active_report"] = None

# ============================================================
# SIDEBAR — RESEARCH HISTORY
# ============================================================

st.sidebar.markdown("## 📚 Research History")
st.sidebar.caption("Load previously generated market reports.")

try:
    history_response = requests.get(
        f"{BACKEND_URL}/research/history",
        timeout=5,
    )
    history_response.raise_for_status()
    history = history_response.json()
except requests.exceptions.RequestException:
    history = []
    st.sidebar.error(
        "Backend not reachable.\n\n"
        "Start FastAPI with:\n"
        "`uvicorn backend.main:app --reload`"
    )

if history:
    st.sidebar.markdown(
        '<div class="history-label">Saved Research</div>',
        unsafe_allow_html=True,
    )

    for item in history:
        label = item["query"]

        if st.sidebar.button(
            label,
            key=f"history_{item['id']}",
            use_container_width=True,
        ):
            try:
                past_response = requests.get(
                    f"{BACKEND_URL}/research/{item['id']}",
                    timeout=10,
                )
                past_response.raise_for_status()
                past = past_response.json()

                st.session_state["active_report"] = {
                    "query": past["query"],
                    "report": past["report"],
                }

                st.rerun()

            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"Could not load report: {e}")
else:
    st.sidebar.info("No saved research yet.")

st.sidebar.markdown("---")
st.sidebar.caption("Agentic Market Research Tool")
st.sidebar.caption("Gemini • Tavily • Trafilatura • SQLite")

# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🔎 Agentic Market Research Tool</div>
        <p class="hero-subtitle">
            AI-powered market research with live web retrieval,
            source-grounded analysis, and persistent research history.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SEARCH AREA
# ============================================================


st.markdown("### 🎯 Start New Research")

if "query_input" not in st.session_state:
    st.session_state["query_input"] = ""

st.write("Try an example:")
example_cols = st.columns(3)

examples = [
    "EV market in India",
    "Plant-based food market trends",
    "Cloud gaming industry",
]

for col, example in zip(example_cols, examples):
    if col.button(example, use_container_width=True):
        st.session_state["query_input"] = example

query = st.text_input(
    "Market research query",
    value=st.session_state["query_input"],
    placeholder="Example: Electric vehicle market in India",
    label_visibility="collapsed",
)

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    run_research = st.button(
        "🚀 Run Research",
        type="primary",
        use_container_width=True,
    )

with col2:
    clear_report = st.button(
        "✕ Clear",
        use_container_width=True,
    )

with col3:
    st.caption(
        "The research pipeline may take up to several minutes "
        "because it plans, searches, collects, and analyzes live sources."
    )


# ============================================================
# CLEAR ACTIVE REPORT
# ============================================================

if clear_report:
    st.session_state["active_report"] = None
    st.rerun()

# ============================================================
# NEW RESEARCH REQUEST
# ============================================================

if run_research:
    if not query.strip():
        st.warning("Please enter a market research query first.")
    else:
        with st.spinner(
            "🤖 Running the agentic research pipeline..."
        ):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/research",
                    json={"query": query.strip()},
                    timeout=180,
                )

                response.raise_for_status()
                result = response.json()

                if result["status"] == "no_data":
                    st.warning(result["message"])
                    st.session_state["active_report"] = None
                else:
                    st.session_state["active_report"] = {
                        "query": result["query"],
                        "report": result["report"],
                    }

                    st.rerun()

            except requests.exceptions.Timeout:
                st.error(
                    "The request timed out. "
                    "The pipeline may be taking longer than expected — "
                    "please try again."
                )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Can't reach the backend. "
                    "Make sure FastAPI is running with:\n\n"
                    "`uvicorn backend.main:app --reload`"
                )

            except requests.exceptions.HTTPError:
                if response.status_code == 429:
                    st.error(
                        "You're sending requests too quickly. "
                        "Please wait a minute and try again."
                    )
                else:
                    st.error(
                        f"Research failed "
                        f"(server returned {response.status_code})."
                    )

            except requests.exceptions.RequestException:
                st.error(
                    "Something went wrong while contacting the research backend. "
                    "Please try again."
                )

# ============================================================
# REPORT DISPLAY
# ============================================================

active = st.session_state.get("active_report")

if active:
    report = active["report"]
    active_query = active["query"]

    key_trends = report.get("key_trends", [])
    sources = report.get("sources_referenced", [])

    # --------------------------------------------------------
    # REPORT HEADER
    # --------------------------------------------------------

    st.markdown(f"## 📊 Research Report")

    st.caption(f"Query: **{active_query}**")

    # --------------------------------------------------------
    # DYNAMIC METRICS
    # --------------------------------------------------------

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Research Status</div>
                <div class="metric-value">Completed ✓</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Key Trends</div>
                <div class="metric-value">{len(key_trends)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Referenced Sources</div>
                <div class="metric-value">{len(sources)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # --------------------------------------------------------
    # MARKET OVERVIEW
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">📈 Market Overview</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(report.get("market_overview", "No market overview available."))

    # --------------------------------------------------------
    # KEY TRENDS
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">🔥 Key Trends</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if key_trends:
        for index, trend in enumerate(key_trends, start=1):
            safe_trend = html.escape(str(trend))
            st.markdown(
                f"""
                <div class="trend-item">
                    <strong>{index:02d}</strong>&nbsp;&nbsp;{safe_trend}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No key trends were identified from the available sources.")

    # --------------------------------------------------------
    # TWO-COLUMN ANALYSIS
    # --------------------------------------------------------

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">🏢 Competitor Landscape</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write(
            report.get(
                "competitor_landscape",
                "No competitor information available.",
            )
        )

    with right_col:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-title">💬 Consumer Sentiment</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write(
            report.get(
                "consumer_sentiment",
                "No consumer sentiment information available.",
            )
        )

    # --------------------------------------------------------
    # RISKS & OPPORTUNITIES
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">⚠️ Risks & Opportunities</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        report.get(
            "risks_opportunities",
            "No risk or opportunity information available.",
        )
    )

    # --------------------------------------------------------
    # SOURCES
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">🔗 Sources Referenced</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if sources:
        with st.expander(
            f"View {len(sources)} referenced source(s)",
            expanded=True,
        ):
            for index, url in enumerate(sources, start=1):
                st.markdown(f"**Source {index}**")
                st.link_button("Open source", url)
                st.divider()
    else:
        st.info(
            "No external sources were referenced in this report. "
            "The system did not fabricate unsupported information."
        )

else:
    # ========================================================
    # EMPTY STATE
    # ========================================================

    st.markdown("## 👋 Welcome")

    st.info(
        "Enter a market research question above to generate a "
        "source-grounded market report."
    )

    st.markdown("### 💡 Example Queries")

    example1, example2, example3 = st.columns(3)

    with example1:
        st.markdown("**⚡ Electric Vehicles**")
        st.caption("EV market in India")

    with example2:
        st.markdown("**🤖 Artificial Intelligence**")
        st.caption("AI market in India")

    with example3:
        st.markdown("**🔐 Cybersecurity**")
        st.caption("Indian cybersecurity market")

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Agentic Market Research Tool • Phase 7 Dashboard
        <br>
        Source-grounded AI research with persistent history
    </div>
    """,
    unsafe_allow_html=True,
)
