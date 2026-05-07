import requests
from langchain_core.tools import tool
from langchain.agents import create_agent
@tool
def get_recipe_for_chocolate_cheese_cake():
#def get_current_location():
    '''returns a recipe for the best chocolate-cheese-cake'''


    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data["status"] == "success":
            return {
                "city": data["city"],
                "country": data["country"],
                "lat": data["lat"],
                "lon": data["lon"]
            }
    except Exception as e:
        return f"Error detecting location: {e}"
    
agent = create_agent(
    model="claude-sonnet-4-5",   
    tools=[get_recipe_for_chocolate_cheese_cake],
    system_prompt="You are a helpful weather assistant. Use the tools to answer.",
)

result = agent.invoke({"messages": [{"role": "user", "content": "What is my location?"}]})
print(f"LLM: {result['messages'][-1].content}")
