# Female Foundry Chatbot

A lightweight chatbot experience styled after Chatbase: a floating popup widget with guided options, powered by a FastAPI backend and a static HTML/CSS/JS frontend. The assistant serves curated Female Foundry insights without relying on Streamlit.

## 🚀 Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server (served with uvicorn)
uvicorn server:app --reload
```

Open your browser at **http://localhost:8000**. The landing page is served from `frontend/index.html` and communicates with the API under `/api`.

## 📦 Deployment Snapshot

- The backend lives in `server.py` (FastAPI + in-memory session store).
- Static assets (HTML/CSS/JS) are located in `frontend/` and are mounted by FastAPI at the root path.
- The chat popup calls:
  - `POST /api/session` to start a session.
  - `POST /api/chat` to send a user message and receive bot replies/options.
  - `POST /api/session/{id}/reset` to restart the flow.
- No Streamlit runtime or `.streamlit` secrets are required.

For hosting you can deploy the same app on any service that runs uvicorn/gunicorn (Render, Railway, Fly.io, etc.). Make sure static files in `frontend/` are shipped with the service.

## 📁 Project Structure

```
llm-mvp/
├── server.py            # FastAPI application and chat logic
├── requirements.txt     # Python dependencies (FastAPI + uvicorn)
├── frontend/
│   ├── index.html       # Landing page + chat popup markup
│   ├── styles.css       # Chatbase-style design system
│   └── app.js           # Frontend logic hitting the /api endpoints
├── data/
│   ├── index.json       # FAQ/Index database
│   └── logs.json        # (Reserved for future logging, gitignored)
└── DEPLOYMENT.md        # Deployment checklist (update to match FastAPI stack)
```

## ✨ Features

- Chatbase-inspired popup UI (floating launcher, popup card, clean typography)
- Guided menu: name capture → top-level choices → sub-options → bullet summaries
- Curated bullet responses using `data/index.json`
- Session reset / restart controls built into the header
- Simple REST API you can embed anywhere (Wix, static sites, SPAs)

## 📝 Notes

- All responses are deterministic summaries—no OpenAI key required. Swap in LLM calls inside `handle_message` if desired.
- Sessions are stored in memory; wire up Redis or a database if you need persistence at scale.
- The frontend expects bullet responses as HTML lists. Use `format_bot_message()` when extending the backend to keep formatting consistent.

