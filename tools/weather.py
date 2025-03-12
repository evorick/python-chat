# tools/weather.py
import requests
import json

# Weather tool schema for the chatbot
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a US location by city name",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name (e.g., 'New York', 'Chicago')"
                }
            },
            "required": ["city"]
        }
    }
}

def get_weather(city):
    """Fetch current weather data for a given US city using the National Weather Service API."""
    try:
        # Step 1: Geocode the city to get latitude/longitude using a simple Nominatim API (OpenStreetMap)
        geocode_url = f"https://nominatim.openstreetmap.org/search?q={city},USA&format=json&limit=1"
        headers = {'User-Agent': 'xAI-Chatbot/1.0'}  # NWS requires a user agent
        geo_response = requests.get(geocode_url, headers=headers)
        geo_data = geo_response.json()
        
        if not geo_data:
            return f"Could not find location data for {city}"
        
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # Step 2: Get the weather forecast from NWS
        points_url = f"https://api.weather.gov/points/{lat},{lon}"
        points_response = requests.get(points_url, headers=headers)
        points_data = points_response.json()
        
        if 'properties' not in points_data:
            return f"Could not fetch weather data for {city}"
        
        # Step 3: Get the forecast from the hourly forecast endpoint
        forecast_url = points_data['properties']['forecastHourly']
        forecast_response = requests.get(forecast_url, headers=headers)
        forecast_data = forecast_response.json()
        
        if 'properties' not in forecast_data or 'periods' not in forecast_data['properties']:
            return f"Could not fetch forecast for {city}"
        
        # Get the current (first) forecast period
        current = forecast_data['properties']['periods'][0]
        temp = current['temperature']
        unit = current['temperatureUnit']
        conditions = current['shortForecast']
        
        return f"Current weather in {city}: {temp}°{unit}, {conditions}"
    
    except Exception as e:
        return f"Error fetching weather for {city}: {str(e)}"