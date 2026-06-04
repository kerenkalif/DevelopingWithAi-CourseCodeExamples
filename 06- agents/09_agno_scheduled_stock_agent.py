import os

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
from agno.scheduler import ScheduleManager

from stock_tools import collect_and_summarize_stocks, write_to_log
from emails_tool import send_gmail

# ── Config ──
DB_FILE        = "tmp/stock.db"
SENDER_EMAIL   = "keren.kalif@gmail.com"
SENDER_PASSKEY = os.environ["GMAIL_APP_PASSWORD_FOR_STOCK_ANALYZER_AGENT"]
RECEIVER_EMAIL = "keren.kalif@gmail.com"


# Agent-facing tool: the model only decides subject/body — the recipient and
# the sender credentials are injected here, so the agent can't email an
# arbitrary address. No confirmation: this agent runs unattended.
def email_alert(subject: str, body: str) -> str:
    """Email a stock alert (to the fixed recipient)."""
    return send_gmail(
        RECEIVER_EMAIL, subject, body,
        sender_email=SENDER_EMAIL,
        sender_name="Stock Agent",
        sender_passkey=SENDER_PASSKEY,
    )


# ── Agent ──
agent_db = SqliteDb(id="stock-agent", db_file=DB_FILE)

stock_agent = Agent(
    id="StockAnalyst",
    name="StockAnalyst",
    model=Claude(id="claude-sonnet-4-6"),
    tools=[
        collect_and_summarize_stocks,
        write_to_log,
        email_alert,
    ],
    description="You are a stock market analyst.",
    instructions=[
        "Call collect_and_summarize_stocks to get current prices and 1h stats.",
        "Analyze the data: identify trends, anomalies, or significant moves.",
        "Call write_to_log with: prices, your analysis, and recommendation if any.",
        "If you identify an urgent buy or sell signal (>0.2% move): send an email alert using email_alert.",
        "Keep analysis concise — 3-5 sentences max.",
    ],
    db=agent_db,
    add_history_to_context=True,
    num_history_runs=3,
)

# ── Scheduler ──
agent_os = AgentOS(
    name="Stock Monitor",
    agents=[stock_agent],
    db=agent_db,
    scheduler=True,
    scheduler_poll_interval=15,
)

mgr = ScheduleManager(agent_db)
mgr.create(
    name="stock-every-minute",
    cron="* * * * *",
    endpoint="/agents/StockAnalyst/runs",
    payload={"message": "Analyze stocks now."},
    if_exists="update",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(agent_os.get_app(), host="0.0.0.0", port=7777)