# 19 - LangGraph - Conditional Edges
# Library: langgraph, langchain-openai
# What it does: Graph branches based on weather — sunny goes one way, rainy another.
#               Demonstrates add_conditional_edges.
# pip install langgraph langchain-openai requests

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import requests

class State(TypedDict):
    city: str
    weather: str
    advice: str


def check_weather(state: State) -> dict:
    url = f"https://wttr.in/{state['city']}?format=3"
    weather = requests.get(url, timeout=5).text
    return {"weather": weather}


def sunny_response(state: State) -> dict:
    return {"advice": f"Perfect day in {state['city']}! Sunscreen recommended. {state['weather']}"}


def rainy_response(state: State) -> dict:
    return {"advice": f"Take an umbrella in {state['city']} today. {state['weather']}"}


# Conditional function — returns the name of the next node
def is_weather_sunny(state: State) -> str:
    weather = state["weather"].lower()
    if any(word in weather for word in ["sun", "clear", "partly cloudy", "fair"]):
        return "sunny_response"
    return "rainy_response"


graph = StateGraph(State)
graph.add_node("check_weather",  check_weather)
graph.add_node("sunny_response", sunny_response)
graph.add_node("rainy_response", rainy_response)

graph.add_edge(START, "check_weather")

# Conditional edge — branching based on weather result
graph.add_conditional_edges("check_weather", is_weather_sunny)

graph.add_edge("sunny_response", END)
graph.add_edge("rainy_response", END)

compiled = graph.compile()

for city in ["Tel Aviv", "London", "Barcelona"]:
    result = compiled.invoke({"city": city})
    print(f"{city}: {result['advice']}")
    print()
