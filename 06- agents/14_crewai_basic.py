# 14 - CrewAI - Basic Agent (Tel Aviv vs Paris comparison)
# Library: crewai
# What it does: Weather analyst compares Tel Aviv and Paris for summer travel.
# pip install crewai openai requests

from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from secret_key import openai_key
import os
import requests

os.environ["OPENAI_API_KEY"] = openai_key


@tool("WeatherTool")
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    url = f"https://wttr.in/{city}?format=3"
    return requests.get(url, timeout=5).text


weather_agent = Agent(
    role="Senior Weather Analyst",
    goal="Provide accurate weather analysis for travel planning",
    backstory="Expert in climate data with 10 years advising travelers.",
    tools=[get_weather],
    verbose=True,
)

task = Task(
    description="Compare summer weather in Tel Aviv and Paris. "
                "Check current conditions for both cities.",
    expected_output="A comparison table with temperature, humidity, conditions. "
                    "End with a clear recommendation: which city is better for summer?",
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
