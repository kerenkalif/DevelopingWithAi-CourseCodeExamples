# 08 - Agno - Memory (SqliteStorage)
# Library: agno
# What it does: Agent that remembers previous conversations across sessions.
#               Run this script twice — the second run will remember the first.
# pip install agno requests sqlalchemy

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.tools import tool
import requests

@tool()
def get_weather(city: str) -> str:
    """Use this tool to get the current weather for a given city."""
    url = f"https://wttr.in/{city}?format=3"
    return requests.get(url, timeout=5).text

db = SqliteDb(db_file="agno.db")
agent = Agent(
    model=Claude(id="claude-sonnet-4-6"),
    db=db,
    add_history_to_context=True,
    num_history_runs=3,                    # load last 3 conversations
    tools=[get_weather],
    description="You are a weather assistant with memory of past conversations.",
    markdown=True,
)

# Run 1: ask about today
#response = agent.run("What is the weather in Tel Aviv today?", session_id="weather_session_user42")
#print(response.content)

# Run 2:
response = agent.run("Which city did we talk about last time?", session_id="weather_session_user42",  )
print(response.content)