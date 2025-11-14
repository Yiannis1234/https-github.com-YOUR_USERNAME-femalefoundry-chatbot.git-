# FastAPI Deployment Guide

This project now ships a FastAPI backend plus a static HTML/CSS/JS frontend. Streamlit is no longer used. Deploying means running a single uvicorn (or gunicorn) process that serves both the API and static assets.

## 🚀 Quick Deploy Steps (Render / Railway / Fly.io / etc.)

1. **Push to GitHub** (or your preferred repo host):
   ```bash
   git add .
   git commit -m "Female Foundry chatbot"
   git push origin main
   ```

2. **Create a new web service** on your hosting provider:
   - **Runtime**: Python 3.10+
   - **Start command**: `uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}`
   - **Environment variables**: none required by default (add your own if you extend the backend)
   - **Working directory**: `llm-mvp/`

3. **Deploy**. The platform builds dependencies from `requirements.txt`, starts uvicorn, and serves:
   - Frontend at `https://<your-app>/` (served from `frontend/`)
   - API at `https://<your-app>/api/...`

## 🧪 Local Smoke Test

```bash
pip install -r requirements.txt
uvicorn server:app --reload
```

Visit http://localhost:8000 to confirm the landing page and chat widget load. The widget calls:
- `POST /api/session` when the page loads
- `POST /api/chat` when you send messages or click quick options
- `POST /api/session/{session_id}/reset` when you tap ↺ in the header

## 📁 Deployment Checklist

- [ ] `server.py` (FastAPI) committed
- [ ] `frontend/` directory committed (index.html, styles.css, app.js)
- [ ] `requirements.txt` contains `fastapi` and `uvicorn`
- [ ] `data/index.json` present (FAQ payload)
- [ ] No Streamlit files needed (`.streamlit/`, `app.py` removed)

## 🔒 Security / Extensibility Notes

- Current build uses curated responses—no OpenAI key required. If you add an LLM call, store the key as an environment variable on your hosting provider.
- Sessions are kept in memory. Swap `SESSIONS` with Redis or your data store if you need persistence or horizontal scaling.
- Static files are served directly by FastAPI; for CDN caching or custom hosting, point your CDN to the `frontend/` directory and point API calls to `/api`.

## 🐛 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `404 Session not found` | Frontend lost its `session_id`. Reset the session (`↺`) or reload the page. |
| Styles/JS not loading in production | Ensure static files are deployed; some platforms require `STATIC_DIR` config or `--root-path`. |
| API blocked by CORS | `server.py` allows `*` origins by default. Tighten later once you know the production domain. |

## 🔄 Updating the App

1. Commit & push changes.
2. Trigger redeploy on your platform (most services do this automatically).
3. Hard refresh the browser (Cmd+Shift+R) to clear cached CSS/JS.

Happy shipping! 🛳️

