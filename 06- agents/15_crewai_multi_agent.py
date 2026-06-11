# 15 - CrewAI - Multi-Agent Sequential + Custom Tool + output_file
# Library: crewai
# What it does: Two agents in sequence — weather_agent collects data,
#               report_writer writes a markdown report saved to a file.
# pip install crewai openai requests

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from pydantic import Field
import requests

# CrewAI's default model is OpenAI (gpt-4) - here we use Claude instead.
# The model string format is "anthropic/<model-id>" (CrewAI uses litellm),
# and the ANTHROPIC_API_KEY is read from the environment.
llm = LLM(model="anthropic/claude-sonnet-4-6")

class WeatherTool(BaseTool):
    name: str = "Weather Tool"
    description: str = "Get current weather for a given city using wttr.in."

    def _run(self, city: str) -> str:
        url = f"https://wttr.in/{city}?format=3"
        return requests.get(url, timeout=5).text


weather_agent = Agent(
    role="Weather Data Collector",
    goal="Collect accurate current weather data for multiple cities",
    backstory="Specialist in gathering and validating real-time weather data.",
    tools=[WeatherTool()],
    llm=llm,
    verbose=True,
)

report_writer = Agent(
    role="Travel Report Writer",
    goal="Write clear and engaging travel weather reports",
    backstory="Experienced travel writer who turns data into compelling recommendations.",
    llm=llm,
    verbose=True,
)

task1 = Task(
    description="Get current weather for: Tel Aviv, Barcelona, Amsterdam.",
    expected_output="Weather data for all 3 cities: temperature, conditions, humidity.",
    agent=weather_agent,
)

task2 = Task(
    description="Write a travel weather report based on the collected data. "
                "Rank the cities from best to worst for a summer vacation.",
    expected_output="A well-structured markdown report with city rankings and reasons.",
    output_file="weather_report.md",   # CrewAI saves output directly to file
    agent=report_writer,
)

crew = Crew(
    agents=[weather_agent, report_writer],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()
print(result)
print("Report saved to: weather_report.md")
