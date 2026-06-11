# 18 - LangGraph - Methodology (State + Nodes + Edges)
# Library: langgraph, requests
# What it does: Minimal graph — one node checks weather for a city stored in State.
#               Demonstrates the 4 core concepts: State, Node, Edge, Graph.
#               No LLM here — LangGraph is provider-agnostic; this example needs no API key.
# pip install langgraph requests

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import os
import requests


# 1. State — shared data that flows through all nodes
class State(TypedDict):
    city: str
    weather: str
    recommendation: str


# 2. Node — a Python function that receives State and returns updated State
def check_weather(state: State) -> dict:
    url = f"https://wttr.in/{state['city']}?format=3"
    weather = requests.get(url, timeout=5).text
    return {"weather": weather}


def make_recommendation(state: State) -> dict:
    weather = state["weather"]
    if any(word in weather.lower() for word in ["sunny", "clear", "partly"]):
        rec = f"Great day to visit {state['city']}! {weather}"
    else:
        rec = f"Maybe skip {state['city']} today. {weather}"
    return {"recommendation": rec}


# 3. Graph — connect nodes with edges
graph = StateGraph(State)
graph.add_node("check_weather",     check_weather)
graph.add_node("make_recommendation", make_recommendation)

# 4. Edges — define the flow
graph.add_edge(START,              "check_weather")
graph.add_edge("check_weather",    "make_recommendation")
graph.add_edge("make_recommendation", END)

compiled = graph.compile()

# Run
result = compiled.invoke({"city": "Tel Aviv"})
print("Weather:       ", result["weather"])
print("Recommendation:", result["recommendation"])
