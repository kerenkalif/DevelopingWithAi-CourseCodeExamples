# 16 - CrewAI - Agent + MCP Server
# Library: crewai, mcp
# What it does: CrewAI agent uses our MCP weather server as a tool.
#               MCPServerAdapter wraps the MCP server — no changes to the server needed.
# pip install crewai crewai-tools mcp openai requests
#
# REQUIRES: weather_mcp_server.py in the same folder (see below)

from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

# CrewAI's default model is OpenAI (gpt-4) - here we use Claude instead.
# The model string format is "anthropic/<model-id>" (CrewAI uses litellm),
# and the ANTHROPIC_API_KEY is read from the environment.
llm = LLM(model="anthropic/claude-sonnet-4-6")

server_params = StdioServerParameters(
    command="python",
    args=["weather_mcp_server.py"],   # our MCP server
)

with MCPServerAdapter([server_params]) as tools:
    weather_agent = Agent(
        role="Weather Expert",
        goal="Answer weather queries using the MCP weather server",
        backstory="Expert in weather data analysis.",
        tools=tools,
        llm=llm,
        verbose=True,
    )

    task = Task(
        description="Get the current weather in Tel Aviv and Paris. "
                    "Which city is better for a summer visit this week?",
        expected_output="Weather comparison with a clear recommendation.",
        agent=weather_agent,
    )

    crew = Crew(
        agents=[weather_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    print(result)
