# Female Foundry Chatbot MVP

A Chatbase-inspired chatbot experience for Female Foundry. The current build uses a FastAPI backend with a static HTML/CSS/JS front-end so it can be embedded anywhere (Wix, static sites, landing pages) without Streamlit or Node runtimes.

## Features

- Floating popup widget with a clean Chatbase-style layout.
- Guided flow: capture visitor name → primary topics → curated sub-options → bullet summaries.
- Responses sourced from `data/index.json` and returned as concise bullet lists.
- REST API (`/api`) that can be consumed by other clients (Wix HTTP functions, SPAs, etc.).
- One-command local run using uvicorn; no additional services required.

## Prerequisites

- Python 3.10+
- pip
- (Optional) Infrastructure to persist sessions or pipe responses into CRM tools.

## Quick Start

```bash
cd "llm-mvp"
pip install -r requirements.txt
uvicorn server:app --reload
```

Open http://localhost:8000 to view the landing page and interact with the popup chat. The widget communicates with:
- `POST /api/session` – start/reset a session
- `POST /api/chat` – send the user’s message and receive bot replies/options

## Project Layout

```
llm-mvp/
├── server.py            # FastAPI app with session handling + curated responses
├── requirements.txt     # Python dependencies (FastAPI, uvicorn)
├── frontend/
│   ├── index.html       # Landing page + chat markup
│   ├── styles.css       # Chatbase-style design system
│   └── app.js           # Frontend logic wired to the /api endpoints
├── data/
│   ├── index.json       # Female Foundry knowledge base
│   └── logs.json        # (Reserved for future logging)
├── QUICK_START.md       # Local/dev instructions
└── DEPLOYMENT.md        # FastAPI deployment checklist
```

## Extending the MVP

- **LLM Integration**: Plug an OpenAI (or other) call inside `handle_message` in `server.py`; use `format_bot_message()` to keep bullet formatting consistent.
- **Data Sources**: Swap `INFO_MAP` content for live data pulled from Wix Data, Airtable, or a headless CMS.
- **Session Storage**: Replace the in-memory `SESSIONS` dict with Redis/DynamoDB if you need persistence or horizontal scaling.
- **Analytics**: Log each exchange to a database or analytics pipeline (e.g., Segment, BigQuery) for reporting.
- **Branding**: Adjust typography, gradients, and copy in `frontend/styles.css` and `index.html` to mirror production designs.

## Demo Script

1. Provide your name (e.g., “Ioannis”) to personalise responses.
2. Click **Female Foundry Programs** → **AI Hustle** – receive a three-bullet summary.
3. Hit ↺ (Start over) to show the reset flow.
4. Close the popup and reopen via the 💬 bubble to demonstrate behaviour on Wix-like pages.

## Next Steps

- Validate copy and CTA destinations with stakeholders.
- Hook the API into your preferred hosting platform (Render, Railway, Fly.io, etc.).
- Test embed in Wix via an iframe or custom element pointing to the hosted widget.
- Layer analytics + CRM handover if the bot escalates unanswered questions.

