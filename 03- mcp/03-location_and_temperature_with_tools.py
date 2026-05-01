import requests
#from langchain_anthropic import ChatAnthropic
from anthropic import Anthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

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
    
def get_weather_in_location(lat: float, lon: float) -> float:
    '''returns current temperature according to coordinate'''
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        return data["current_weather"]["temperature"]
    except Exception as e:
        return f"Error fetching weather: {e}"
    
tools = [
    {
        "name": "get_current_location",
        "description": "Returns the user's location based on their IP.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "get_coordinates",
        "description": "Gets a city name and returns its coordinates.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city_name":    {"type": "string"},
                "country_name": {"type": "string"}
            },
            "required": ["city_name"]
        }
    },
    {
        "name": "get_weather_in_location",
        "description": "Returns the current temperature for given coordinates.",
        "input_schema": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lon": {"type": "number"}
            },
            "required": ["lat", "lon"]
        }
    }
]

tool_impls = {
    "get_current_location":    get_current_location,
    "get_coordinates":         get_coordinates,
    "get_weather_in_location": get_weather_in_location,
}


# ============================================================
# 4. The loop
# ============================================================
client = Anthropic()

def run_with_tools(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )

        print(f"1- stop reason: {response.stop_reason}")
        # If the model is done — return its final text answer
        if response.stop_reason == "end_turn":
            return "".join(block.text for block in response.content if block.type == "text")

        # Otherwise — execute every tool the model asked for
        print(f"2- response.content: {response.content}")
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  -> calling {block.name}({block.input})")    # for teaching
                result = tool_impls[block.name](**block.input)
                tool_results.append({
                    "type":        "tool_result",
                    "tool_use_id": block.id,
                    "content":     str(result),
                })
        messages.append({"role": "user", "content": tool_results})


# ============================================================
# 5. Try it
# ============================================================
print(run_with_tools("what is the temperature at my place?"))
print()
print(run_with_tools("how warm is it in London right now?"))
print()
print(run_with_tools("compare the temperature in Tel Aviv and Paris"))