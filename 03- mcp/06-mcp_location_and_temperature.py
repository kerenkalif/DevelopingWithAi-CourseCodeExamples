import requests
from mcp.server.fastmcp import FastMCP
from anthropic import Anthropic

# creating the MCP server
mcp = FastMCP("WeatherService")

@mcp.tool()
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
    
@mcp.tool()
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
    
@mcp.tool()
def get_weather_in_location(lat: float, lon: float) -> float:
    '''returns current temperature according to coordinate'''
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        return data["current_weather"]["temperature"]
    except Exception as e:
        return f"Error fetching weather: {e}"
    

if __name__ == "__main__":
    #mcp.run()
    mcp.run(transport='sse')

    client = Anthropic()

    test_prompts = ["what is the temperature at my place?",
                    "how warm is it in London right now?",
                    "compare the temperature in Tel Aviv and Paris",
                   ]
    
    for prompt in test_prompts:
        print(f"Prompt --> {prompt}")
        messages = [{"role": "user", "content": prompt}]

        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=messages,
        )
        print(f"LLM --> {response.content[0].text}")

    