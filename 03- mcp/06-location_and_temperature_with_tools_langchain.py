import requests
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool

@tool
def get_current_location():
    '''returns user current geographic location according to its ip'''
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
    
@tool
def get_coordinates(city_name: str, country_name: str = ""):
    '''  gets city name and country, and returns its coordinates '''
    try:
        query = f"{city_name}, {country_name}" if country_name else city_name
            
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=1&language=en&format=json"
        
        response = requests.get(url)
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "lat": result["latitude"],
                "lon": result["longitude"],
                "full_name": f"{result.get('name')}, {result.get('country')}"
            }
        else:
            return "Location not found."
            
    except Exception as e:
        return f"Error connecting to geocoding service: {e}"
    
@tool
def get_weather_in_location(lat: float, lon: float) -> float:
    '''returns current temperature according to coordinate'''
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        return data["current_weather"]["temperature"]
    except Exception as e:
        return f"Error fetching weather: {e}"
    
tools_list = [get_current_location, get_coordinates, get_weather_in_location]
llm = ChatAnthropic(model="claude-sonnet-4-5")
llm_with_tools = llm.bind_tools(tools_list)

tool_impls = {
    "get_current_location":    get_current_location,
    "get_coordinates":         get_coordinates,
    "get_weather_in_location": get_weather_in_location,
}
tool_impls = {t.name: t for t in tools_list}


def run_with_tools(user_message: str) -> str:

    messages = [{"role": "user", "content": user_message}]
    while True:
        response = llm_with_tools.invoke(messages)
        if not response.tool_calls:
            return response.content

        messages.append(response)
        for tc in response.tool_calls:
            #result = tool_impls[tc["name"]](**tc["args"])
            result = tool_impls[tc["name"]].invoke(tc["args"])
            messages.append({
                "role":         "tool",
                "tool_call_id": tc["id"],
                "content":      str(result),
            })

# ============================================================
# 5. Try it
# ============================================================
test_prompts = ["what is the temperature at my place?",
                  #  "how warm is it in London right now?",
                  #  "compare the temperature in Tel Aviv and Paris",
                   ]

for prompt in test_prompts:
    print(f"User: {prompt}")
    print(f"LLM: {run_with_tools(prompt)}")
    print()
