# Agentic Market Research Tool

An AI-powered market research application that plans research queries, searches live web sources, collects webpage content, and generates a source-grounded market research report.

## Live Demo

**Streamlit Frontend:**
https://agentic-market-reseaech-tool-dqchpsrmeccxqf93gcayg7.streamlit.app/

**FastAPI Backend:**
https://agentic-market-reseaech-tool-2.onrender.com/

**API Documentation:**
https://agentic-market-reseaech-tool-2.onrender.com/docs

## Architecture

```text
Streamlit Community Cloud
        |
        v
Render FastAPI Backend
        |
        +--> Gemini
        |
        +--> Tavily
        |
        +--> Trafilatura
        |
        v
SQLite research history




Main Features
AI-generated research plans
Live web search with Tavily
Webpage extraction with Trafilatura
Source-grounded Gemini analysis
Structured market reports
Research history
Rate limiting
Input validation and sanitization
Prompt-injection-aware source handling
User-friendly error handling
Interactive example queries
Local Development

Activate the virtual environment:

source venv/bin/activate

Start the FastAPI backend:

uvicorn backend.main:app --reload

In another terminal, start Streamlit:

streamlit run frontend/app.py
Environment Variables

The application requires:

GEMINI_API_KEY
TAVILY_API_KEY

For local development, store these in .env.

Do not commit API keys or other secrets to GitHub.

Deployment

The FastAPI backend is deployed on Render.

The Streamlit frontend is deployed on Streamlit Community Cloud.

The frontend communicates with the Render backend using an explicit CORS allowlist.

Known Deployment Limitation

The backend currently uses SQLite for research history.

The free Render service uses ephemeral filesystem storage, so SQLite data should not be considered permanent production storage. Research history can be lost when the service is restarted or recreated.

For permanent production history, the application should be migrated to a managed persistent database such as PostgreSQL.

Technology Stack
Python
FastAPI
Streamlit
Google Gemini API
Tavily
Trafilatura
SQLAlchemy
SQLite
SlowAPI
Project Structure
agentic-market-research-tool/
├── backend/
│   ├── agent.py
│   ├── analyzer.py
│   ├── collector.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── reporter.py
│   └── search.py
├── frontend/
│   └── app.py
├── requirements.txt
├── requirements-render.txt
├── SECURITY.md
├── README.md
└── .gitignore
Phase 10 Deployment Status

The application has been deployed and verified end-to-end.

Live Streamlit frontend:

https://agentic-market-reseaech-tool-dqchpsrmeccxqf93gcayg7.streamlit.app/

Live FastAPI backend:

https://agentic-market-reseaech-tool-2.onrender.com/

FastAPI documentation:

https://agentic-market-reseaech-tool-2.onrender.com/docs
