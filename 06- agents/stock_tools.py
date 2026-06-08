import yfinance as yf
import sqlite3
from datetime import datetime, timedelta
from agno.tools import tool

# ── Config ──
PRICE_DB = "tmp/stock_prices.db"
LOG_FILE = "tmp/stock_log.txt"
STOCKS   = {"NVIDIA": "NVDA", "Apple": "AAPL", "Google": "GOOGL"}

# ── DB init ──
def init_price_db():
    con = sqlite3.connect(PRICE_DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            ts TEXT, symbol TEXT, price REAL
        )
    """)
    con.commit(); 
    con.close()

# ── Tools ──
def collect_and_summarize_stocks() -> str:
    """Fetch current prices, save to DB, return stats summary of last hour"""
    init_price_db()
    con = sqlite3.connect(PRICE_DB)
    ts = datetime.now().isoformat()

    # 1. save current values
    for name, symbol in STOCKS.items():
        price = round(yf.Ticker(symbol).fast_info.last_price, 2)
        con.execute("INSERT INTO prices VALUES (?,?,?)", (ts, symbol, price))
    con.commit()

    # 2. calculate statistics from last hour
    cutoff = (datetime.now() - timedelta(hours=1)).isoformat()
    lines = []
    for name, symbol in STOCKS.items():
        rows = con.execute(
            "SELECT price FROM prices WHERE symbol=? AND ts>=? ORDER BY ts",
            (symbol, cutoff)
        ).fetchall()
        if len(rows) < 2:
            lines.append(f"{name}: ${rows[-1][0]} (not enough data yet)")
            continue
        prices = [r[0] for r in rows]
        change_pct = round((prices[-1] - prices[0]) / prices[0] * 100, 2)
        lines.append(
            f"{name}: ${prices[-1]} | "
            f"1h change: {change_pct:+.2f}% | "
            f"min: ${min(prices)} | max: ${max(prices)}"
        )
    con.close()
    return "\n".join(lines)

def write_to_log(content: str) -> str:
    """Persist the analysis to the log file (a side effect, for record keeping)."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"\n[{ts}]\n{content}\n" + "-"*50)
    return "Log updated"

@tool(stop_after_tool_call=True, show_result=True)
def present_analysis(analysis: str) -> str:
    """Present the final analysis to the user. This is the agent's LAST step.
    The 'analysis' you pass here is exactly what the user sees, so it must be the
    clean analysis only — no preamble or commentary, 3-5 sentences. Calling this
    ends the run, so nothing is appended after it."""
    return analysis
