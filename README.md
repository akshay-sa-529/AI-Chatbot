# Free 24/7 AI Chatbot

A complete, ready-to-run AI chatbot: Flask backend + a clean chat widget UI,
powered by a **free** LLM API. No paid services required to build or run it.

## What's inside
```
free-ai-chatbot/
├── app.py              # Flask backend, talks to the AI API
├── templates/index.html
├── static/style.css
├── static/script.js
├── requirements.txt
├── Procfile             # for Render/Railway
├── .env.example
└── README.md
```

## 1. Get a free AI API key
This project defaults to **Groq** — free, no credit card, and very fast:
1. Go to https://console.groq.com
2. Sign up, then create an API key under "API Keys"
3. Free models available include `llama-3.1-8b-instant` and `llama-3.3-70b-versatile`

Other free options you can swap in (see "Swapping providers" below):
- **Google AI Studio (Gemini)** — free tier: https://aistudio.google.com
- **Hugging Face Inference API** — free tier: https://huggingface.co/settings/tokens
- **OpenRouter** — several free models: https://openrouter.ai
- **Ollama** — run a model fully offline/locally, $0 forever, but only "24/7" if your own machine stays on: https://ollama.com

## 2. Run it locally (test first)
```bash
cd free-ai-chatbot
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then edit .env and paste your GROQ_API_KEY
python app.py
```
Open http://localhost:5000 — you should see the chat widget working.

## 3. Deploy it for free, 24/7

### Option A — Render.com (recommended, easiest)
1. Push this folder to a GitHub repo.
2. Go to https://render.com → New → Web Service → connect your repo.
3. Build command: `pip install -r requirements.txt`
   Start command: `gunicorn app:app`
4. Add environment variables (Render dashboard → Environment):
   `GROQ_API_KEY`, `MODEL`, `SECRET_KEY`
5. Deploy. You'll get a free URL like `https://yourapp.onrender.com`

**Free-tier caveat (important, honest note):** Render's free web services
sleep after ~15 minutes of no traffic, then take ~30-50 seconds to wake up
on the next request. To keep it awake around the clock:
- Create a free account at https://uptimerobot.com
- Add a monitor that pings `https://yourapp.onrender.com/health` every 5 minutes
This keeps the app "warm" so it responds instantly, at no cost.

### Option B — Railway.app
Similar flow to Render; free tier gives a monthly usage allowance rather
than unlimited always-on hours, so check current limits before relying on
it for heavy 24/7 traffic.

### Option C — Fly.io
Fly's free allowance can run a small VM continuously without the
sleep/wake behavior Render has, at the cost of a slightly more involved
CLI-based deployment (`fly launch`, `fly deploy`).

### Option D — Your own always-on machine (Raspberry Pi, old laptop, home server)
Run `python app.py` (or better, `gunicorn app:app`) behind a tool like
`pm2` or a systemd service, and use a free dynamic DNS service (e.g. No-IP)
if you want a stable public URL. Truly free and fully in your control, but
uptime depends on your own hardware/internet staying on.

## 4. Swapping providers (optional)
`app.py` calls an OpenAI-compatible `/chat/completions` endpoint. To switch:
- **Gemini**: use Google's OpenAI-compatibility endpoint, or the `google-generativeai` SDK, and adjust `GROQ_URL`/`MODEL`/auth header accordingly.
- **OpenRouter**: set `GROQ_URL = "https://openrouter.ai/api/v1/chat/completions"` and use an OpenRouter key + a free model like `meta-llama/llama-3.1-8b-instruct:free`.
- **Ollama (local)**: set `GROQ_URL = "http://localhost:11434/v1/chat/completions"`, no API key needed, but the machine running Ollama must stay on.

## 5. Ideas to extend this
- Add a knowledge base: paste your FAQs/docs into the `SYSTEM_PROMPT` in `app.py` so the bot answers from your content.
- Embed it on your existing website: point an `<iframe src="https://yourapp.onrender.com">` at your deployed chatbot, or copy the widget's HTML/CSS/JS into your site and just call your backend's `/api/chat` route.
- Add streaming responses, file uploads, or persistent chat history (swap Flask's in-memory session for a free database like Supabase or SQLite).
- Add simple rate-limiting (e.g. `Flask-Limiter`) before you share the link publicly, so free API quota isn't burned by one heavy user.

## Cost summary
- **Code/hosting**: $0 (Render/Railway/Fly free tiers)
- **AI API**: $0 (Groq/Gemini/OpenRouter free tiers — each has daily/rate limits, generous enough for a personal or small-project chatbot)
- **Keep-alive pings**: $0 (UptimeRobot free tier)

Nothing here requires a credit card to get started. Free tiers do have
rate limits, so under heavy traffic you may eventually want a paid plan —
but for personal projects, prototypes, and small sites, this setup runs
indefinitely for free.
