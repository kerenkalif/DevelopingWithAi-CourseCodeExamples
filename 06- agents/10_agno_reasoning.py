# 09 - Agno - Agent Reasoning (ThinkingTools)
# Library: agno
# What it does: Agent that shows its full reasoning chain — every decision visible.
#               Useful for debugging why the agent took certain actions.
# pip install agno openai requests

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from agno.tools.thinking import ThinkingTools
from secret_key import openai_key
import os
import requests

os.environ["OPENAI_API_KEY"] = openai_key


@tool()
def get_weather(city: str) -> str:
    """Use this tool to get the current weather for a given city."""
    url = f"https://wttr.in/{city}?format=3"
    return requests.get(url, timeout=5).text


@tool()
def get_location() -> str:
    """Use this tool to get the user current location."""
    return "Tel Aviv, Israel"


agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        ThinkingTools(add_instructions=True),  # exposes reasoning steps
        get_weather,
        get_location,
    ],
    description="You are a weather planning assistant.",
    markdown=True,
)

agent.print_response(
    "Plan my outdoor activities for this week based on the weather forecast",
    show_full_reasoning=True,       # shows Think → Act → Observe → Reflect
    stream_intermediate_steps=True,
    stream=True,
)
