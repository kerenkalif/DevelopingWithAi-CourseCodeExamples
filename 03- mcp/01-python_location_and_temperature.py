import requests

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
    

my_location_data = get_current_location()
print(my_location_data)
current_temperature = get_weather_in_location(my_location_data["lat"], my_location_data["lon"])
print(f"The current temperature at {my_location_data["city"]} ({my_location_data["country"]}) is {current_temperature }°C.")
print("1~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

location_coordinate = get_coordinates("Tel Aviv", "Israel") # doesn't find
print(location_coordinate)
current_temperature = get_weather_in_location(location_coordinate["lat"], location_coordinate["lon"])
print(f"The current temperature at {location_coordinate["full_name"]} {current_temperature }°C.")

print("2~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
location_coordinate = get_coordinates("Paris", "England")
print(location_coordinate)
current_temperature = get_weather_in_location(location_coordinate["lat"], location_coordinate["lon"])
print(f"The current temperature in {location_coordinate["full_name"]} {current_temperature }°C.")
print("3~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

location_coordinate = get_coordinates("Paris", "France") 
# בדיקה שהחזרה היא אכן מילון ולא הודעת שגיאה
if isinstance(location_coordinate, dict):
    current_temperature = get_weather_in_location(location_coordinate["lat"], location_coordinate["lon"])
    print(f"The current temperature at {location_coordinate["full_name"]} {current_temperature }°C.")
else:
    print(f"Could not find coordinates: {location_coordinate}")
    