# 10 - Agno - Multi-Agent Team
# Library: agno
# What it does: A team of 3 agents — Researcher finds destinations,
#               WeatherChecker checks conditions, Evaluator decides if result is good.
#               If not good enough, the Coordinator sends agents back for another round.
# pip install agno openai duckduckgo-search requests

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools import tool
from agno.team import Team
import requests

@tool()
def get_weather(city: str) -> str:
    """Use this tool to get the current weather for a given city."""
    url = f"https://wttr.in/{city}?format=3"
    return requests.get(url, timeout=5).text


researcher = Agent(
    name="Researcher",
    role="Find popular summer travel destinations in Europe",
    model=Claude(id="claude-sonnet-4-6"),
    #tools=[DuckDuckGoTools()],
    instructions=["Search for top summer destinations with pleasant weather"],
)

weather_checker = Agent(
    name="WeatherChecker",
    role="Check current weather conditions for given cities",
    model=Claude(id="claude-sonnet-4-6"),
    tools=[get_weather],
    instructions=["Check weather for each city. Flag cities above 35C as too hot."],
)

evaluator = Agent(
    name="Evaluator",
    role="Evaluate if the weather results are good enough for a summer vacation",
    model=Claude(id="claude-sonnet-4-6"),
    instructions=[
        "Check if we have at least 3 cities with pleasant weather (20-30C, no rain).",
        "If not enough options found, ask the Researcher to search for more cities.",
    ],
)

team = Team(
    name="VacationPlannerTeam",
    mode="coordinate",                   # Coordinator decides who does what at runtime
    model=Claude(id="claude-sonnet-4-6"),
    members=[researcher, weather_checker, evaluator],
    instructions=[
        "Find the best summer vacation destination with comfortable weather.",
        "Keep searching until you have at least 3 good options.",
    ],
    markdown=True,
)

team.print_response(
    "Find me a summer vacation destination with pleasant weather — not too hot, no rain.",
    stream=True)

pass

response = team.run("Find me a summer vacation destination with pleasant weather — not too hot, no rain.")
print(response.content)
