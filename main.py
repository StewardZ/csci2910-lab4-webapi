import requests
import json

# API URLs
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# API usage to find city cordinates
def geocode_city(city_name):
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    print("\n GEOCODING REQUEST ")
    print("Endpoint:", GEOCODE_URL)
    print("Parameters Sent:")
    print(json.dumps(params, indent=4))

    response = requests.get(GEOCODE_URL, params=params)

    print("\n GEOCODING RESPONSE (RAW JSON RECEIVED) ")
    print(json.dumps(response.json(), indent=4))

    data = response.json()

    if "results" not in data:
        return None

    result = data["results"][0]

    return {
        "name": result["name"],
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "country": result.get("country"),
        "admin1": result.get("admin1")
    }

# API usage to find weather forecast for cities cordinates
def get_forecast(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "temperature_unit": "fahrenheit",
        "timezone": "auto"
    }

    print("\n FORECAST REQUEST ")
    print("Endpoint:", FORECAST_URL)
    print("Parameters Sent:")
    print(json.dumps(params, indent=4))

    response = requests.get(FORECAST_URL, params=params)

    print("\n FORECAST RESPONSE (RAW JSON RECEIVED) ")
    print(json.dumps(response.json(), indent=4))

    data = response.json()

    daily = data.get("daily", {})

    forecast_days = []

    for i in range(len(daily.get("time", []))):
        forecast_days.append({
            "date": daily["time"][i],
            "tmax": daily["temperature_2m_max"][i],
            "tmin": daily["temperature_2m_min"][i],
            "precip": daily["precipitation_sum"][i]
        })

    return forecast_days

# main program to print JSON and weather forecast
def main():
    print(" Weather Forecast Program (Open-Meteo) ")

    city = input("\nEnter a city name: ")

    location = geocode_city(city)

    if not location:
        print("\nCity not found")
        return

    print("\nLocation Found:")
    print(f"{location['name']}, {location.get('admin1', '')}, {location.get('country', '')}")

    forecast_data = get_forecast(location["latitude"], location["longitude"])

    print("\n FORMATTED FORECAST OUTPUT ")

    for day in forecast_data:
        print(f"\n|Date: {day['date']}|")
        print(f"  |High: {day['tmax']}°F|")
        print(f"  |Low:  {day['tmin']}°F|")
        print(f"  |Precipitation: {day['precip']}|")

# program start
if __name__ == "__main__":
    main()

    
