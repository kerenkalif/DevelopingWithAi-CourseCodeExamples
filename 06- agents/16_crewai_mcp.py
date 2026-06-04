# 16 - CrewAI - Agent + MCP Server
# Library: crewai, mcp
# What it does: CrewAI agent uses our MCP weather server as a tool.
#               MCPServerAdapter wraps the MCP server — no changes to the server needed.
# pip install crewai crewai-tools mcp openai requests
#
# REQUIRES: weather_mcp_server.py in the same folder (see below)

from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from secret_key import openai_key
import os

os.environ["OPENAI_API_KEY"] = openai_key

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
