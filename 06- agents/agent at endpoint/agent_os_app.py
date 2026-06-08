from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from stock_tools import collect_and_summarize_stocks, write_to_log, present_analysis

# ── Agent ──
agent_db = SqliteDb(id="stock-agent", db_file="tmp/stock.db")

stock_agent = Agent(
    id="StockAnalyst",
    name="StockAnalyst",
    model=Claude(id="claude-sonnet-4-20250514"),
    tools=[collect_and_summarize_stocks, write_to_log, present_analysis],
    description="You are a stock market analyst.",
    instructions=[
        "Call collect_and_summarize_stocks to get current prices and 1h stats.",
        "Analyze the data: identify trends, anomalies, or significant moves.",
        "Call write_to_log to persist your analysis (3-5 sentences) to the log.",
        "Then call present_analysis with that same clean analysis as your LAST step.",
        "The text you pass to present_analysis is exactly what the user sees —",
        "only the analysis itself, no preamble or commentary.",
    ],
    db=agent_db,
    add_history_to_context=False,
)

# ── AgentOS ──
agent_os = AgentOS(
    name="Stock Monitor",
    agents=[stock_agent],
    db=agent_db,
    cors_allowed_origins=[
        "http://127.0.0.1:5500", "http://localhost:5500",   # Live Server
        "http://127.0.0.1:8000", "http://localhost:8000",   # python http.server
        "null",                                              # file://
    ],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(agent_os.get_app(), host="0.0.0.0", port=7777)
