# 21 - LangGraph - Multi-Node Pipeline with an LLM in each node
# Library: langgraph, langchain-anthropic, requests
# What it does: The LangGraph translation of CrewAI example 15 (multi-agent sequential).
#               Two nodes run in sequence, each calling Claude:
#                 1. collect_weather - fetches raw weather (tool) + LLM structures it
#                 2. write_report    - LLM writes a markdown report, saved to a file
# pip install langgraph langchain-anthropic requests
#
# CrewAI 15 vs. this file - same idea, two different styles:
#   CrewAI:    you declare Agents + Tasks, the framework orchestrates them.
#   LangGraph: YOU wire the graph explicitly; each node decides to call the model.
#
# ANTHROPIC_API_KEY is read from the environment (same as the CrewAI examples).

from typing import TypedDict
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
import requests

# One shared model for both nodes (unlike CrewAI, the LLM is OUR choice per node).
llm = ChatAnthropic(model="claude-sonnet-4-6")


# 1. State - shared data that flows through the nodes
class State(TypedDict):
    cities: list[str]
    weather_data: str   # filled by node 1
    report: str         # filled by node 2


# 2. Node 1 - "Weather Data Collector" (CrewAI: weather_agent)
#    Fetches raw weather (the "tool"), then the LLM cleans it into structured data.
def collect_weather(state: State) -> dict:
    raw = []
    for city in state["cities"]:
        url = f"https://wttr.in/{city}?format=3"
        raw.append(requests.get(url, timeout=5).text)
    raw_text = "\n".join(raw)

    response = llm.invoke(
        "Here is raw weather data for several cities:\n"
        f"{raw_text}\n\n"
        "Turn this into a clean summary listing each city with its "
        "temperature and conditions."
    )
    return {"weather_data": response.content}


# 3. Node 2 - "Travel Report Writer" (CrewAI: report_writer)
#    No tool here - just the LLM, turning data into a ranked markdown report.
def write_report(state: State) -> dict:
    response = llm.invoke(
        "Write a travel weather report in markdown based on this data:\n"
        f"{state['weather_data']}\n\n"
        "Rank the cities from best to worst for a summer vacation, "
        "with a short reason for each."
    )
    report = response.content
    with open("weather_report_langgraph.md", "w", encoding="utf-8") as f:
        f.write(report)
    return {"report": report}


# 4. Graph - wire the two nodes in sequence (CrewAI: Process.sequential)
graph = StateGraph(State)
graph.add_node("collect_weather", collect_weather)
graph.add_node("write_report",    write_report)

graph.add_edge(START,             "collect_weather")
graph.add_edge("collect_weather", "write_report")
graph.add_edge("write_report",    END)

compiled = graph.compile()

# Run
result = compiled.invoke({"cities": ["Tel Aviv", "Barcelona", "Amsterdam"]})
print(result["report"])
print("\nReport saved to: weather_report_langgraph.md")
