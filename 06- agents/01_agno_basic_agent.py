
from agno.agent import Agent
from agno.models.anthropic import Claude

agent = Agent(
    model=Claude(id="claude-sonnet-4-6"),
    description="You are a weather expert. Answer questions about weather and climate.",
    markdown=True,
)

response = agent.run("Is Tel Aviv hot in summer? What should I wear?")
print(response.content)