"""
Binance Market Intelligence Agent
===================================
Powered by Groq (LLaMA 3.3 70B) + Binance Public API
Built for MUST Company Quest Submission
"""

import os
import requests
from groq import Groq
from dotenv import load_dotenv
from ddgs import DDGS
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

GROQ_MODEL = "llama-3.3-70b-versatile"
TOP_COINS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
             "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "DOTUSDT", "MATICUSDT"]
MOVER_THRESHOLD = 2.0

BINANCE_ENDPOINTS = [
    "https://api.binance.com/api/v3/ticker/24hr",
    "https://api1.binance.com/api/v3/ticker/24hr",
    "https://api2.binance.com/api/v3/ticker/24hr",
    "https://api3.binance.com/api/v3/ticker/24hr",
]

def fetch_binance_data() -> list[dict]:
    """
    Tries multiple Binance endpoints (some regions block certain ones).
    Falls back gracefully if all fail.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    for endpoint in BINANCE_ENDPOINTS:
        try:
            print(f"Trying endpoint: {endpoint}")
            # Fetch each coin individually to avoid region blocks on batch calls
            coins = []
            for symbol in TOP_COINS:
                resp = requests.get(
                    endpoint,
                    params={"symbol": symbol},
                    headers=headers,
                    timeout=10
                )
                if resp.status_code == 200:
                    item = resp.json()
                    coins.append({
                        "symbol": item["symbol"].replace("USDT", ""),
                        "pair": item["symbol"],
                        "price": float(item["lastPrice"]),
                        "change_pct": float(item["priceChangePercent"]),
                        "change_usd": float(item["priceChange"]),
                        "high_24h": float(item["highPrice"]),
                        "low_24h": float(item["lowPrice"]),
                        "volume_usdt": float(item["quoteVolume"]),
                    })

            if coins:
                coins.sort(key=lambda x: abs(x["change_pct"]), reverse=True)
                return coins

        except Exception as e:
            print(f"Endpoint failed: {e}")
            continue

    # Last resort: use CoinGecko (no region restrictions)
    return fetch_from_coingecko()


def fetch_from_coingecko() -> list[dict]:
    """
    Fallback to CoinGecko public API — no region restrictions at all.
    """
    try:
        print("Trying CoinGecko fallback...")
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": "bitcoin,ethereum,binancecoin,solana,ripple,cardano,dogecoin,avalanche-2,polkadot,matic-network",
            "order": "market_cap_desc",
            "price_change_percentage": "24h"
        }
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()

        coins = []
        for item in data:
            change_pct = item.get("price_change_percentage_24h") or 0
            price = item.get("current_price") or 0
            coins.append({
                "symbol": item["symbol"].upper(),
                "pair": item["symbol"].upper() + "USDT",
                "price": price,
                "change_pct": change_pct,
                "change_usd": item.get("price_change_24h") or 0,
                "high_24h": item.get("high_24h") or 0,
                "low_24h": item.get("low_24h") or 0,
                "volume_usdt": item.get("total_volume") or 0,
            })

        coins.sort(key=lambda x: abs(x["change_pct"]), reverse=True)
        print(f"CoinGecko: got {len(coins)} coins")
        return coins

    except Exception as e:
        print(f"CoinGecko also failed: {e}")
        return []


def get_big_movers(coins: list[dict]) -> list[dict]:
    return [c for c in coins if abs(c["change_pct"]) >= MOVER_THRESHOLD]


def fetch_news(symbol: str) -> list[dict]:
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(f"{symbol} crypto news today", max_results=3):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")[:300]
                })
        return results
    except Exception:
        return []


def generate_briefing(coins: list[dict], movers: list[dict], news_map: dict) -> str:
    market_lines = []
    for c in coins:
        arrow = "▲" if c["change_pct"] > 0 else "▼"
        market_lines.append(
            f"  {c['symbol']}: ${c['price']:,.4f} {arrow} {c['change_pct']:+.2f}% | Vol: ${c['volume_usdt']/1e6:.1f}M"
        )
    market_summary = "\n".join(market_lines)

    news_context = ""
    for mover in movers[:3]:
        sym = mover["symbol"]
        articles = news_map.get(sym, [])
        if articles:
            news_context += f"\n{sym} News:\n"
            for a in articles:
                news_context += f"  - {a['title']}: {a['snippet']}\n"

    prompt = f"""You are a professional crypto market analyst giving a morning briefing to a trading desk.

Current Date/Time: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}

LIVE MARKET DATA (24h change):
{market_summary}

NOTABLE MOVERS NEWS:
{news_context if news_context else "No specific news found for movers."}

Write a sharp, professional market briefing (200-250 words) covering:
1. Overall market sentiment (bullish/bearish/mixed) and why
2. The top 2-3 movers — what's driving them based on the news
3. One key thing to watch in the next 24 hours
4. One actionable insight for a trader/investor

Use clear, direct language. No fluff. Sound like a Bloomberg analyst, not a chatbot."""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a sharp, professional crypto market analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content


def run_analysis() -> dict:
    coins = fetch_binance_data()
    if not coins:
        return {"error": "Could not fetch market data from Binance or CoinGecko. Please try again in a moment."}

    movers = get_big_movers(coins)
    news_map = {}
    for mover in movers[:3]:
        news_map[mover["symbol"]] = fetch_news(mover["symbol"])

    briefing = generate_briefing(coins, movers, news_map)

    return {
        "timestamp": datetime.now().strftime("%B %d, %Y at %H:%M UTC"),
        "coins": coins,
        "movers": movers,
        "news_map": news_map,
        "briefing": briefing,
        "error": None
    }


if __name__ == "__main__":
    print("\n🚀 Binance Market Intelligence Agent")
    print("=" * 50)
    result = run_analysis()
    if result.get("error"):
        print(f"❌ {result['error']}")
    else:
        print(f"\n📅 {result['timestamp']}")
        print("\n📊 TOP COINS:")
        for c in result["coins"]:
            arrow = "▲" if c["change_pct"] > 0 else "▼"
            print(f"  {c['symbol']:8} ${c['price']:>12,.4f}  {arrow} {c['change_pct']:+.2f}%")
        print(f"\n🤖 AI BRIEFING:\n")
        print(result["briefing"])