# 🚀 FASTAPI QUICK START

## ✅ What's Ready
- ✅ FastAPI server (`server.py`)
- ✅ Static frontend (`frontend/index.html`, `styles.css`, `app.js`)
- ✅ Data payload (`data/index.json`)
- ✅ Requirements file (`requirements.txt` with FastAPI + uvicorn)

---

## 📋 RUN LOCALLY

```bash
cd "llm-mvp"

# Install dependencies
pip install -r requirements.txt

# Start the app (serves API + frontend)
uvicorn server:app --reload
```

Visit: http://localhost:8000

You should see the landing page with the floating chat popup. The API lives under `/api` (e.g. `POST /api/chat`).

---

## ☁️ DEPLOY IN 3 STEPS

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Female Foundry FastAPI chatbot"
   git push origin main
   ```

2. **Create a web service** (Render, Railway, Fly.io, etc.)
   - Runtime: Python 3.10+
   - Start command: `uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}`
   - Working directory: `llm-mvp/`
   - Environment variables: none required (add your own if extending the backend)

3. **Deploy** and share the generated URL (frontend and API are served from the same app).

---

## 🔍 TROUBLESHOOTING

| Issue | Fix |
| --- | --- |
| 404 on `/api/chat` | Ensure the server is running at the same origin; avoid proxies stripping `/api`. |
| CSS/JS not updating | Hard refresh (Cmd+Shift+R) or clear cache after redeploy. |
| "Session not found" | The chat lost its `session_id`. Click ↺ (Start over) or reload the page. |
| CORS errors | Adjust the `CORSMiddleware` config in `server.py` if you deploy frontend elsewhere. |

---

## 📁 FILES YOU NEED

- ✅ `server.py`
- ✅ `frontend/index.html`, `frontend/styles.css`, `frontend/app.js`
- ✅ `requirements.txt`
- ✅ `data/index.json`
- ✅ `.gitignore` (optional but recommended)

---

## 🎯 NEXT STEPS

- Tailor copy/branding in the landing page (`frontend/index.html`).
- Add analytics/logging via the backend session store.
- Integrate an actual LLM call inside `handle_message` if you want dynamic answers.

Happy building! 💬

