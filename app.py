# chatbot app.py

import os
import requests
from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = os.environ.get("MODEL", "llama-3.1-8b-instant")  # groc model

SYSTEM_PROMPT = (
    "You are a Richi, a friendly ,helpful assistant embedded in a website chat widget. "
    "Keep answers concise and clear."
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    if not GROQ_API_KEY:
        return jsonify({"error": "Server missing GROQ_API_KEY. See README.md."}), 500

    data = request.get_json(force=True)
    user_message = (data or {}).get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    
    history = session.get("history", [])
    history.append({"role": "user", "content": user_message})
    history = history[-10:]  

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        resp = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"model": MODEL, "messages": messages, "temperature": 0.7},
            timeout=30,
        )
        resp.raise_for_status()
        reply = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return jsonify({"error": f"Upstream error: {e}"}), 502

    history.append({"role": "assistant", "content": reply})
    session["history"] = history

    return jsonify({"reply": reply})


@app.route("/api/reset", methods=["POST"])
def reset():
    session.pop("history", None)
    return jsonify({"status": "ok"})

# app awake 24/7 on free 
@app.route("/health")
def health():
    return jsonify({"status": "alive"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
