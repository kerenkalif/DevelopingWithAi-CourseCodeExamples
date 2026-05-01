import requests
from langchain_anthropic import ChatAnthropic
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
    

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
parser = StrOutputParser()

# Each function becomes a station in the chain
add_coords  = RunnableLambda(
    lambda x: {**x, **get_coordinates(x["city"])}
)
add_weather = RunnableLambda(
    lambda x: {**x, "temp": get_weather_in_location(x["lat"], x["lon"])}
)

prompt = ChatPromptTemplate.from_template(
    "The weather in {city} is {temp} degrees Celsius."
)

# JSON flows from station to station — each one adds fields
#chain = add_coords | add_weather | prompt | llm | StrOutputParser()
chain = add_coords | add_weather | prompt | StrOutputParser()

result = chain.invoke({"city": "Tel Aviv"})
print(result)