from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def geocode_city(city_name):
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(GEOCODE_URL, params=params)
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


def get_forecast(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "temperature_unit": "fahrenheit",
        "timezone": "auto"
    }

    response = requests.get(FORECAST_URL, params=params)
    data = response.json()

    daily = data.get("daily", {})

    forecast_days = []

    for i in range(len(daily["time"])):
        forecast_days.append({
            "date": daily["time"][i],
            "tmax": daily["temperature_2m_max"][i],
            "tmin": daily["temperature_2m_min"][i],
            "precip": daily["precipitation_sum"][i]
        })

    return forecast_days


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/forecast", methods=["POST"])
def forecast():
    city = request.form.get("city")

    location = geocode_city(city)

    if not location:
        return render_template("index.html", error="City not found.")

    forecast_data = get_forecast(location["latitude"], location["longitude"])

    location_name = f"{location['name']}, {location.get('admin1', '')}, {location.get('country', '')}"

    return render_template("forecast.html",
                           location=location_name,
                           days=forecast_data)


if __name__ == "__main__":

    app.run(debug=True)
