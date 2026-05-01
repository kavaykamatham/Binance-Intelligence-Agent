# 📡 Binance Market Intelligence Agent

> An AI agent that monitors live Binance markets, detects unusual price movements,
> fetches breaking news, and delivers a professional plain-English briefing —
> powered by Groq LLaMA 3.3 70B.

**🔴 Live Demo**: https://binance-intelligence-agent-hgpu3gqn9a3x5kjfzzf96v.streamlit.app/

---

## 🎯 Problem This Solves

A crypto trader or APO at MUST Company needs to answer one question every morning:

> *"What's moving in the market, why is it moving, and what should I do about it?"*

Answering this manually means:
- Checking 10+ coin prices on Binance
- Reading 5-10 news articles
- Synthesizing it all into a decision

**This agent does all of that in under 10 seconds.**

---

## ❓ Why I Chose This Problem

MUST Company explicitly listed **Binance Integration** as their #1 current priority.

This agent is not a generic demo — it's a tool that an APO at MUST Company would
open every morning before making product decisions. It directly embodies the role:

> *"APO uses AI agents to automate research and reduce friction between idea and execution."*

**This is priority definition in action:** I chose the problem MOST relevant to
MUST Company's stated work — not the easiest or most common submission.

---

## 🚀 What It Does

1. **Fetches live prices** of top 10 coins from Binance public API (no account needed)
2. **Detects movers** — coins with >2% price change in 24h
3. **Auto-searches news** for each notable mover using DuckDuckGo
4. **Runs Groq AI** (LLaMA 3.3 70B) to generate a professional market briefing
5. **Displays everything** in a clean dark-themed Streamlit dashboard
6. **Auto-refresh mode** available for continuous monitoring

---

## ⚡ Quick Start (Local)

### 1. Clone
```bash
git clone https://github.com/YOUR_USERNAME/binance-agent.git
cd binance-agent
```

### 2. Install
```bash
pip install -r requirements.txt
```

### 3. Set up API key
```bash
cp .env.example .env
# Open .env and add your Groq key
# Get free key at: https://console.groq.com
```

### 4. Run dashboard
```bash
streamlit run app.py
```

### 5. Or run CLI mode
```bash
python agent.py
```

---

## ☁️ Deploy to Streamlit Cloud (Free — Get a Live Link)

1. Push this repo to GitHub (public)
2. Go to **https://share.streamlit.io**
3. Click **"New app"** → select your repo → set main file to `app.py`
4. Go to **Settings → Secrets** and add:
   ```
   GROQ_API_KEY = "your_key_here"
   ```
5. Click **Deploy** — you get a live public URL in ~2 minutes

---

## 🏗️ Architecture

```
app.py (Streamlit Dashboard)
  │
  └── agent.py (Core Pipeline)
        │
        ├── fetch_binance_data()
        │     └── Binance Public API (no auth needed)
        │
        ├── get_big_movers()
        │     └── Filter coins with |change%| > 2.0%
        │
        ├── fetch_news(symbol)
        │     └── DuckDuckGo search → top 3 articles
        │
        └── generate_briefing()
              └── Groq LLaMA 3.3 70B → plain-English analysis
```

---

## 📁 File Structure

```
binance-agent/
├── agent.py          # Core agent pipeline
├── app.py            # Streamlit dashboard
├── requirements.txt  # Python dependencies
├── .cursorrules      # Cursor AI configuration
├── .env.example      # API key template
├── .gitignore        # Keeps secrets safe
├── metrics.md        # Performance score: 8,640/10,000
├── benchmark.md      # Comparison vs default Claude/Cursor
└── README.md         # This file
```

---

## 📊 Performance Score

**8,640 / 10,000** — See [metrics.md](./metrics.md) for full methodology.

Key highlights:
- Groq inference: ~1.2 seconds
- Full pipeline: ~8 seconds
- 96% success rate over 50 test runs

---

## 🔒 Security

- API keys stored in `.env` (local) or Streamlit Secrets (cloud)
- Both are in `.gitignore` — never committed to GitHub
- Binance data uses public API only — no trading permissions required

---

## 🛠️ Cursor Configuration

Open in Cursor — `.cursorrules` is pre-configured with:
- Code style preferences
- Architecture constraints
- Security rules
- Streamlit UI guidelines

---

## 🔮 Roadmap

- [ ] Add RSI / MACD technical indicators from Binance kline data
- [ ] Price alert system (email/Slack notification when threshold hit)
- [ ] Portfolio tracker with custom coin list
- [ ] Historical briefing archive
- [ ] Telegram bot integration
