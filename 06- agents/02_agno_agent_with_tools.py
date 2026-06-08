import asyncio
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

async def main():
    async with MCPTools(
        command="python my_weather_mcp_server.py"
    ) as mcp_tools:
        agent = Agent(
            model=Claude(id="claude-sonnet-4-6"),
            description="You are a weather expert. Use the tools to get current weather data.",
            tools=[mcp_tools],
            markdown=True,
        )
        response = await agent.arun(
            "What is the current weather in my location now?"
        )
        print(response.content)


if __name__ == "__main__":
    asyncio.run(main())