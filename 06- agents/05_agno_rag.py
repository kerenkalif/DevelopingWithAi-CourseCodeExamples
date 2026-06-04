# pip install agno anthropic openai lancedb tantivy pylance pypdf
# pip install timezonefinder geopy pytz

import requests
import os

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.tools import tool

@tool()
def get_weather(city: str) -> str:
    """ Use this tool to get current
        weather for a given city. """
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url)
    return response.text

knowledge = Knowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="travel_guide",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    )
)

if not os.path.exists("tmp/lancedb/travel_guide.lance"):
    knowledge.insert(path="travel_guide.pdf")

agent = Agent(
    model=Claude(id="claude-sonnet-4-6"),
    description="You are a travel assistant.",
    instructions=[
        "ONLY recommend activities that appear explicitly in your knowledge base.",
        "Do NOT use your general knowledge to suggest activities.",
        "If the knowledge base has no information about a city, say so clearly.",
        "Always check the current weather before recommending activities.",
        "Match activities to the current weather conditions based on the knowledge base guidelines.",
    ],
    knowledge=knowledge,
    tools=[get_weather],
)

response = agent.run(
    "I'm visiting London today. "
    "What activities do you recommend for the current weather?"
)

print(response.content)