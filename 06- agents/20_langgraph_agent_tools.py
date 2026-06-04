# 20 - LangGraph - Agent + Tools (ReAct loop)
# Library: langgraph, langchain-openai
# What it does: LangGraph agent with tools — LLM decides when to call get_weather
#               and recommend_destination. Uses tools_condition for automatic routing.
# pip install langgraph langchain-openai requests

from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AnyMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from secret_key import openai_key
import os
import requests

os.environ["OPENAI_API_KEY"] = openai_key


@tool()
def get_weather(city: str) -> str:
    """Get the current weather for a given city. Use this to check conditions."""
    url = f"https://wttr.in/{city}?format=3"
    return requests.get(url, timeout=5).text


@tool()
def recommend_destination(weather_summary: str) -> str:
    """Given a summary of weather data for multiple cities,
    recommend the best destination for a summer vacation."""
    # In a real scenario this could call another LLM or scoring logic
    return f"Based on the weather data: {weather_summary[:200]}... recommendation: choose the city with 20-28C and no rain."


tools = [get_weather, recommend_destination]
tool_node = ToolNode(tools)
model = ChatOpenAI(model="gpt-4o").bind_tools(tools)


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def run_llm(state: State) -> dict:
    return {"messages": [model.invoke(state["messages"])]}


def run_recommendation(state: State) -> dict:
    return {"messages": [model.invoke(state["messages"])]}


graph = StateGraph(State)
graph.add_node("llm",            run_llm)
graph.add_node("tools",          tool_node)
graph.add_node("llm_recommend",  run_recommendation)

graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", tools_condition)   # auto-routes to tools or END
graph.add_edge("tools", "llm_recommend")
graph.add_edge("llm_recommend", END)

compiled = graph.compile()

result = compiled.invoke({
    "messages": [HumanMessage(
        "Check the weather in Tel Aviv, Barcelona, and Amsterdam. "
        "Which city should I visit this summer?"
    )]
})

for msg in result["messages"]:
    if hasattr(msg, "content") and msg.content:
        print(msg.content)
        print()
