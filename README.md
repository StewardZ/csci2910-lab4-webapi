# csci2910-lab4-webapi
Weather terminal app using Open-Meteo API (CSCI 2910 Lab 4)

## Project Overview
This project is a terminal application that integrates the Open-Meteo API.

The user enters a city name, and the app:
1. Calls the Open-Meteo Geocoding API to convert the city into latitude/longitude
2. Calls the Open-Meteo Forecast API to retrieve a 7-day forecast
3. Displays the forecast in a table in the terminal

This demonstrates how a server-side Python application can make API requests and use JSON responses.

## Technologies Used
- Python 3.9
- JSON
- requests
- Open-Meteo API

## API Endpoints Used

### 1) Geocoding Endpoint
City name to coordinates

Example request:
https://geocoding-api.open-meteo.com/v1/search?name=Johnson%20City&count=1&language=en&format=json

### 2) Forecast Endpoint
Coordinates to daily forecast

Example request:
https://api.open-meteo.com/v1/forecast?latitude=36.3134&longitude=-82.3535&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&temperature_unit=fahrenheit&timezone=auto

## Where API Calls Occur in Code
Both API calls occur inside the `/forecast` route in `main.py`.

- API Call #1 happens in `geocode_city()`
- API Call #2 happens in `get_forecast()`

## Issues
### Issue 1
At first, the city search would fail if the API returned no results. I fixed it by checking if `"results"` exists before trying to use it.

### Issue 2
I had trouble understanding how the forecast data was structured because it comes back as arrays. I solved it by looping through the `daily["time"]` list and pulling values from the matching indexes.

### Issue 3
I improved the user experience by adding a simple error message on the home page when a city is not found.

### Issue 4
Updated the printed forecast in the terminal for improved user readability.

## What I Learned
This lab helped me understand how backend applications talk to external services using HTTP requests. It also gave me practice reading JSON responses and turning API data into something useful on a webpage.

## Final Reflection
Working with a real API made it clear how common APIs are in everyday apps and showed how important it is to learn to how to debug and fix issue that come about since one little issue can throw it all off.
