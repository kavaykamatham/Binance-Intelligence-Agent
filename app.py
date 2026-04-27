"""
Binance Market Intelligence Agent — Streamlit Dashboard
=========================================================
A professional, dark-themed trading intelligence dashboard.
"""

import streamlit as st
import time
from datetime import datetime
from agent import run_analysis

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Binance Intelligence Agent",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Dark terminal / trading aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #080c14;
    color: #e2e8f0;
}

.stApp {
    background: #080c14;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem; max-width: 1400px; }

/* Header */
.header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0 1.5rem 0;
    border-bottom: 1px solid #1e3a5f;
    margin-bottom: 1.5rem;
}
.header-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: -0.5px;
}
.header-sub {
    font-size: 0.75rem;
    color: #475569;
    font-family: 'Space Mono', monospace;
    margin-top: 2px;
}
.live-badge {
    background: #052e16;
    border: 1px solid #166534;
    color: #4ade80;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    padding: 4px 10px;
    border-radius: 4px;
    letter-spacing: 1px;
}

/* Coin cards */
.coin-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin-bottom: 1.5rem;
}
.coin-card {
    background: #0d1520;
    border: 1px solid #1e2d45;
    border-radius: 8px;
    padding: 14px 16px;
    transition: border-color 0.2s;
}
.coin-card:hover { border-color: #38bdf8; }
.coin-card.mover-up { border-color: #166534; background: #0a1f12; }
.coin-card.mover-down { border-color: #7f1d1d; background: #1a0a0a; }
.coin-symbol {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    color: #94a3b8;
    margin-bottom: 6px;
}
.coin-price {
    font-family: 'Space Mono', monospace;
    font-size: 1.05rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 4px;
}
.coin-change {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
}
.coin-change.up { color: #4ade80; }
.coin-change.down { color: #f87171; }
.coin-vol {
    font-size: 0.7rem;
    color: #475569;
    margin-top: 4px;
    font-family: 'Space Mono', monospace;
}

/* Briefing box */
.briefing-box {
    background: #0d1520;
    border: 1px solid #1e3a5f;
    border-left: 3px solid #38bdf8;
    border-radius: 8px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.5rem;
}
.briefing-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #38bdf8;
    letter-spacing: 2px;
    margin-bottom: 0.8rem;
    text-transform: uppercase;
}
.briefing-text {
    font-size: 0.95rem;
    line-height: 1.75;
    color: #cbd5e1;
}

/* News section */
.news-card {
    background: #0d1520;
    border: 1px solid #1e2d45;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.news-coin-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #f59e0b;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.news-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 4px;
    line-height: 1.4;
}
.news-snippet {
    font-size: 0.75rem;
    color: #64748b;
    line-height: 1.5;
}
.news-url {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #38bdf8;
    margin-top: 6px;
    word-break: break-all;
}

/* Section headers */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #475569;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 6px;
    border-bottom: 1px solid #1e2d45;
}

/* Stat boxes */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 1.5rem;
}
.stat-box {
    background: #0d1520;
    border: 1px solid #1e2d45;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
}
.stat-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: #38bdf8;
}
.stat-label {
    font-size: 0.7rem;
    color: #475569;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Refresh button */
.stButton > button {
    background: #0f2744;
    border: 1px solid #1e3a5f;
    color: #38bdf8;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 1px;
    padding: 8px 20px;
    border-radius: 6px;
    width: 100%;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #1e3a5f;
    border-color: #38bdf8;
}

/* Loading spinner */
.loading-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #38bdf8;
    text-align: center;
    padding: 3rem;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = None
if "loading" not in st.session_state:
    st.session_state.loading = False


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
    <div>
        <div class="header-title">📡 BINANCE INTELLIGENCE AGENT</div>
        <div class="header-sub">AI-POWERED MARKET BRIEFING // POWERED BY GROQ + LLAMA 3.3</div>
    </div>
    <div class="live-badge">● LIVE</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONTROLS
# ─────────────────────────────────────────────
col_btn, col_time, col_refresh = st.columns([1, 3, 1])

with col_btn:
    run_btn = st.button("⚡ RUN ANALYSIS", use_container_width=True)

with col_time:
    if st.session_state.data and not st.session_state.data.get("error"):
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#475569;padding-top:10px;">
        LAST UPDATE: {st.session_state.data['timestamp']}
        </div>""", unsafe_allow_html=True)

with col_refresh:
    auto = st.checkbox("Auto-refresh (60s)", value=False)


# ─────────────────────────────────────────────
# RUN ANALYSIS
# ─────────────────────────────────────────────
if run_btn or (auto and st.session_state.data is None):
    with st.spinner(""):
        st.markdown('<div class="loading-text">FETCHING BINANCE DATA + RUNNING AI ANALYSIS...</div>', unsafe_allow_html=True)
        st.session_state.data = run_analysis()

# Auto refresh
if auto and st.session_state.data:
    time.sleep(60)
    st.session_state.data = run_analysis()
    st.rerun()


# ─────────────────────────────────────────────
# DISPLAY RESULTS
# ─────────────────────────────────────────────
data = st.session_state.data

if data is None:
    st.markdown("""
    <div style="text-align:center;padding:4rem;font-family:'Space Mono',monospace;color:#1e3a5f;font-size:0.85rem;letter-spacing:2px;">
        PRESS ⚡ RUN ANALYSIS TO BEGIN
    </div>
    """, unsafe_allow_html=True)

elif data.get("error"):
    st.error(f"❌ {data['error']}")

else:
    coins = data["coins"]
    movers = data["movers"]
    news_map = data["news_map"]
    briefing = data["briefing"]

    # ── STATS ROW ──
    gainers = len([c for c in coins if c["change_pct"] > 0])
    losers = len([c for c in coins if c["change_pct"] < 0])
    total_vol = sum(c["volume_usdt"] for c in coins) / 1e9
    top_mover = max(coins, key=lambda x: abs(x["change_pct"]))

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-box">
            <div class="stat-value" style="color:#4ade80">{gainers}</div>
            <div class="stat-label">Gainers</div>
        </div>
        <div class="stat-box">
            <div class="stat-value" style="color:#f87171">{losers}</div>
            <div class="stat-label">Losers</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">${total_vol:.1f}B</div>
            <div class="stat-label">Total Volume (24h)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── AI BRIEFING ──
    st.markdown('<div class="section-header">🤖 AI Market Briefing</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="briefing-box">
        <div class="briefing-label">GROQ // LLAMA 3.3 70B ANALYSIS</div>
        <div class="briefing-text">{briefing.replace(chr(10), '<br>')}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── COIN CARDS ──
    st.markdown('<div class="section-header">📊 Live Prices — Top 10 Coins</div>', unsafe_allow_html=True)

    mover_symbols = {m["symbol"] for m in movers}
    cards_html = '<div class="coin-grid">'
    for c in coins:
        direction = "up" if c["change_pct"] > 0 else "down"
        arrow = "▲" if c["change_pct"] > 0 else "▼"
        card_class = ""
        if c["symbol"] in mover_symbols:
            card_class = "mover-up" if c["change_pct"] > 0 else "mover-down"

        # Format price
        if c["price"] >= 100:
            price_str = f"${c['price']:,.2f}"
        elif c["price"] >= 1:
            price_str = f"${c['price']:.3f}"
        else:
            price_str = f"${c['price']:.5f}"

        vol_str = f"${c['volume_usdt']/1e6:.0f}M vol"

        cards_html += f"""
        <div class="coin-card {card_class}">
            <div class="coin-symbol">{c['symbol']}</div>
            <div class="coin-price">{price_str}</div>
            <div class="coin-change {direction}">{arrow} {c['change_pct']:+.2f}%</div>
            <div class="coin-vol">{vol_str}</div>
        </div>"""

    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # ── NEWS FOR MOVERS ──
    if news_map:
        st.markdown('<div class="section-header">📰 News — Notable Movers</div>', unsafe_allow_html=True)
        news_col1, news_col2 = st.columns(2)
        col_toggle = True

        for symbol, articles in news_map.items():
            if not articles:
                continue
            col = news_col1 if col_toggle else news_col2
            col_toggle = not col_toggle
            with col:
                for article in articles:
                    st.markdown(f"""
                    <div class="news-card">
                        <div class="news-coin-label">{symbol}</div>
                        <div class="news-title">{article['title']}</div>
                        <div class="news-snippet">{article['snippet']}</div>
                        <div class="news-url">{article['url'][:70]}...</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── NO MOVERS MESSAGE ──
    if not movers:
        st.markdown("""
        <div style="text-align:center;padding:1.5rem;font-family:'Space Mono',monospace;
                    color:#475569;font-size:0.75rem;letter-spacing:1px;border:1px solid #1e2d45;
                    border-radius:8px;background:#0d1520;">
            NO SIGNIFICANT MOVERS DETECTED — MARKET IS CONSOLIDATING
        </div>
        """, unsafe_allow_html=True)

    # ── FOOTER ──
    st.markdown("""
    <div style="margin-top:2rem;padding-top:1rem;border-top:1px solid #1e2d45;
                font-family:'Space Mono',monospace;font-size:0.65rem;color:#334155;
                display:flex;justify-content:space-between;">
        <span>BINANCE INTELLIGENCE AGENT // MUST COMPANY QUEST SUBMISSION</span>
        <span>DATA: BINANCE PUBLIC API // AI: GROQ LLAMA 3.3 70B</span>
    </div>
    """, unsafe_allow_html=True)
