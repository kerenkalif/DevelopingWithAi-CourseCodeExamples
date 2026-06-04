import requests
from agno.agent import Agent
from agno.tools import tool
from agno.models.anthropic import Claude

@tool()
def get_weather(city: str) -> str:
    """ Use this tool to get current
        weather for a given city. """
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url)
    return response.text

agent = Agent(
    model=Claude(id="claude-sonnet-4-6"),
    tools=[get_weather],
    description="Weather assistant"
)

response = agent.run("What should I wear in Tel Aviv today?")
print(response.content)