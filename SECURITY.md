# Threat Model — Agentic Market Research Tool

## Phase 8 Security Hardening

### Scope

This document describes the security threats considered for the
Agentic Market Research Tool and the mitigations implemented during
Phase 8.

The application accepts user-controlled research queries, retrieves
untrusted web content, sends collected content to Gemini for analysis,
and uses external Gemini and Tavily APIs.

---

## Assets

### 1. Gemini and Tavily API Keys

API keys provide access to external services and may create cost and
abuse risk if exposed.

### 2. Research Query History

Research queries are persisted in the local SQLite database
(`research.db`).

### 3. Generated Research Reports

Structured market reports and associated source information are also
stored in `research.db`.

---

## Threats and Mitigations

### 1. Prompt Injection via Scraped Web Content

**Threat:**

A malicious or compromised webpage may contain text designed to
manipulate the language model, such as instructions to ignore previous
instructions, reveal system instructions, or follow attacker-controlled
directives.

**Mitigation:**

The Gemini analysis prompt explicitly separates trusted instructions
from untrusted source material.

Retrieved webpages are treated as data to analyze, not instructions to
follow. The analyzer is instructed not to follow directives contained
inside scraped content.

A second defense layer was added in `backend/collector.py`.
Suspicious instruction-like patterns are detected and logged.

The heuristic detector is a monitoring mechanism, not a source-blocking
mechanism, because legitimate articles may discuss prompt injection as
a topic.

---

### 2. API Key Exposure

**Threat:**

Exposed Gemini or Tavily API keys could allow unauthorized API usage or
billing abuse.

**Mitigation:**

API credentials remain in `.env` rather than application source code.

`.env` is excluded from Git through `.gitignore`.

The Phase 8 audit verified:

- `.env` has no Git history
- no credential files are tracked
- no obvious API-key logging statements are present
- `research.db` and `venv/` remain ignored

API keys are not intentionally returned in API responses.

---

### 3. Resource Abuse / Denial of Wallet

**Threat:**

Repeated automated requests to `POST /research` could trigger repeated
Gemini and Tavily usage and consume external API quotas or costs.

**Mitigation:**

`slowapi` rate limiting is applied to the `/research` endpoint:

**5 requests per minute per client IP address.**

The limiter operates at the API boundary before the expensive research
pipeline is allowed to run.

---

### 4. Information Disclosure Through Errors

**Threat:**

Unhandled exceptions may expose internal file paths, implementation
details, library information, or stack traces to API clients.

**Mitigation:**

The research pipeline is wrapped in exception handling.

Detailed failures are kept server-side while clients receive the
generic message:

`Research pipeline failed. Please try again.`

Missing historical records now return an HTTP `404` response instead of
an application-level error dictionary.

---

### 5. Cross-Site Scripting / Unsafe Rendering

**Threat:**

Scraped or LLM-generated content could contain malicious HTML or
JavaScript that becomes dangerous if inserted into raw HTML.

**Mitigation:**

Normal textual report fields are rendered through Streamlit's normal
text rendering.

Dynamic key-trend values are HTML-escaped before insertion into the
existing presentation HTML.

Dynamic source links were changed from Markdown URL construction to
Streamlit's native `st.link_button()`.

The dashboard's existing static HTML/CSS presentation remains because
those blocks do not directly interpolate scraped article text.

---

## Input Validation and Sanitization

The API request model enforces:

- minimum query length: 3 characters
- maximum query length: 300 characters
- surrounding whitespace removal
- rejection of empty or whitespace-only input

Validation occurs at the Pydantic request boundary before the query
reaches the research pipeline.

---

## Security Testing Performed

Phase 8 included local, credit-free verification for:

- query sanitization
- minimum and maximum query length
- whitespace-only input rejection
- suspicious-content detection
- source-context construction
- FastAPI application import
- rate limiter attachment
- missing-record HTTP 404 behavior
- generic error disclosure behavior
- Streamlit link-rendering capability
- API-key/Git-history hygiene

No unnecessary Gemini or Tavily requests were used for these local
security checks.

---

## Privacy and Current Deployment Limitation

The application stores research queries, sources, and generated reports
in a local SQLite database.

The current database has no user authentication or access control.

Therefore the current design is suitable for local/demo use and is not
a multi-tenant production security model.

---

## Security Limitations

The prompt-injection detector is heuristic and is not guaranteed to
detect obfuscated or previously unseen attacks.

Prompt-level trusted/untrusted separation is therefore treated as the
primary defense, with heuristic detection providing additional
visibility.

Rate limiting is IP-based and is intended to reduce straightforward
request abuse; it is not a substitute for authentication or stronger
production traffic controls.

---

## Phase 8 Security Goal

The goal of Phase 8 is to add practical defense-in-depth to the existing
agentic pipeline without redesigning the completed Phase 0–7
architecture.
