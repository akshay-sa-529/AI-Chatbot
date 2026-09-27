# richi.ai

A simple AI chatbot I built with Flask and Groq's free API. It's got a clean
chat widget, remembers the conversation while you're chatting, and runs
completely free — no paid API keys, no paid hosting.

## What it does

- Chat interface right in the browser
- Talks to an LLM (using Groq's free tier, currently `openai/gpt-oss-20b`)
- Keeps short-term memory of the conversation per session
- Reset button to start a fresh chat
- Deployed for free and stays online 24/7

## Tech stack

- **Backend:** Python + Flask
- **Frontend:** Plain HTML/CSS/JS (no framework, kept it lightweight)
- **AI:** Groq API (OpenAI-compatible, free tier)
- **Hosting:** Render (free web service)
- **Uptime:** UptimeRobot pings to keep it from sleeping

## Running it locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your own Groq API key (get one free at
console.groq.com). Then:

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

## Deploying

Pushed to GitHub and deployed on Render's free tier. Environment variables
(`GROQ_API_KEY`, `MODEL`, `SECRET_KEY`) are set in Render's dashboard, not
committed to the repo — `.env` is git-ignored.

Render's free tier sleeps after 15 minutes of no traffic, so I added an
UptimeRobot monitor pinging `/health` every 5 minutes to keep it responsive.

## Notes

Groq occasionally retires older models — if you get a 404 on the chat
endpoint, check console.groq.com/docs/models for the current list and
update `MODEL` in your `.env`.

## License

MIT — do whatever you want with it.
