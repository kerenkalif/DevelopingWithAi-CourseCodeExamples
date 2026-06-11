# 14 - CrewAI - Agent + Task + Crew (methodology demo)
# Library: crewai
# What it does: A single weather analyst agent finds the best summer destination in Europe.
#               Demonstrates the 3-object CrewAI pattern: Agent → Task → Crew.
# pip install crewai requests

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import requests

# CrewAI's default model is OpenAI (gpt-4) - here we use Claude instead.
# The model string format is "anthropic/<model-id>" (CrewAI uses litellm),
# and the ANTHROPIC_API_KEY is read from the environment.
llm = LLM(model="anthropic/claude-sonnet-4-6")

@tool("WeatherTool")
def get_weather(city: str) -> str:
    """Get the current weather for a given city using wttr.in."""
    url = f"https://wttr.in/{city}?format=3"
    return requests.get(url, timeout=5).text


weather_agent = Agent(
    role="Senior Weather Analyst",
    goal="Analyze weather conditions across European cities and recommend "
         "the best summer travel destinations",
    backstory="You have 10 years of experience analyzing climate data "
              "and advising travelers on the best destinations.",
    tools=[get_weather],
    llm=llm,
    verbose=True,
)

task = Task(
    description="Compare summer weather in Amsterdam, Lisbon, and Dubrovnik. "
                "Check current conditions for each city.",
    expected_output="A comparison table with temperature, conditions, and humidity "
                    "for each city, followed by a clear recommendation.",
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
print("----------------------")
print(result.raw)
