import requests
from openai import OpenAI
import json

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
        "type": "function",
        "function": {
            "name": "get_current_location",
            "description": "Returns the user's location based on their IP.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_coordinates",
            "description": "Gets a city name and returns its coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name":    {"type": "string"},
                    "country_name": {"type": "string"}
                },
                "required": ["city_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_in_location",
            "description": "Returns the current temperature for given coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number"},
                    "lon": {"type": "number"}
                },
                "required": ["lat", "lon"]
            }
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
client = OpenAI()

def run_with_tools(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.chat.completions.create(
                        model="gpt-4o",
                        tools=tools,
                        messages=messages,
                    )

        finish_reason = response.choices[0].finish_reason
        print(f"1- finish_reason: {finish_reason}")

        if finish_reason == "stop":
            return response.choices[0].message.content

        # Otherwise — execute every tool the model asked for
        print(f"2- response.choices[0].message: {response.choices[0].message}")

        assistant_msg = response.choices[0].message
        messages.append(assistant_msg)

        for tool_call in assistant_msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)   # arguments are a JSON string!
            print(f"  -> calling {name}({args})")
            result = tool_impls[name](**args)
            messages.append({
                "role":         "tool",
                "tool_call_id": tool_call.id,
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
