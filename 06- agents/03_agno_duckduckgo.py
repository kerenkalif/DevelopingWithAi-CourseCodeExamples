from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Claude(id="claude-sonnet-4-6"),
    description="You are a weather expert.",
    tools=[DuckDuckGoTools()],
    markdown=True,
)

#response = agent.run("Current weather in Tel Aviv?", stream=False)
response = agent.run("How is Tel Aviv in the summer?", stream=False)
print(response.content)
