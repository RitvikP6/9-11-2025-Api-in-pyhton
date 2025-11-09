# Weather Checker Application using Open-Meteo API
import requests

# Open-Meteo APIs for Geocoding (City -> Coordinates) and Forecast (Coordinates -> Weather)
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def get_simple_condition(wmo_code):
    """Converts common WMO codes to simple descriptions."""
    codes = {
        0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
        61: "Rain (Slight)", 63: "Rain (Moderate)", 71: "Snow (Slight)", 95: "Thunderstorm"
    }
    return codes.get(wmo_code, "Mixed/Other Condition")

def get_weather(city_name):
    """Fetches the current temperature, condition, and humidity for the given city."""
    city_name = city_name.strip()
    if not city_name:
        return "Please enter a city name."

    try:
        # 1. Look up Coordinates (Geocoding)
        geo_params = {'name': city_name, 'count': 1}
        geo_response = requests.get(GEOCODING_URL, params=geo_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get('results'):
            return f"City '{city_name}' not found."

        # Get the first result's coordinates
        location = geo_data['results'][0]
        latitude, longitude = location['latitude'], location['longitude']
        city_display = location.get('name', city_name)
        country = location.get('country', 'N/A')
        
        # 2. Get Weather Forecast
        forecast_params = {
            'latitude': latitude,
            'longitude': longitude,
            # Updated: Requesting 'relative_humidity_2m' in addition to temp and code
            'current': 'temperature_2m,weather_code,relative_humidity_2m',
            'temperature_unit': 'celsius'
        }
        
        forecast_response = requests.get(FORECAST_URL, params=forecast_params)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        # Extract data
        temp = forecast_data['current'].get('temperature_2m')
        code = forecast_data['current'].get('weather_code')
        # New: Extracting humidity
        humidity = forecast_data['current'].get('relative_humidity_2m')
        unit = forecast_data['current_units']['temperature_2m']
        
        condition = get_simple_condition(code)
        
        # Return the simplified output string
        return (
            f"\n-- {city_display}, {country} --\n"
            f"Temperature: {temp}{unit}\n"
            f"Condition:   {condition}\n"
            f"Humidity:    {humidity}%\n" # Added humidity line
        )

    except requests.exceptions.RequestException as e:
        # Simplified error message for connection or bad HTTP status
        return f"Error fetching weather data. Please check connection or city name. ({e})"
    except Exception as e:
        # Catch any other data processing errors
        return f"An unexpected error occurred: {e}"


def main():
    print("Hello! Welcome to the Weather Checker! ")

    while True:
        user_input = input("Enter a city name (or 'q' to quit): ").strip()

        if user_input.lower() in ['q', 'exit']:
            print("Thankyou for using my weather app. Goodbye!")
            break
        elif user_input:
            # The original structure of calling the function and printing the result is kept.
            weather = get_weather(user_input)
            print(weather)
        # Empty input is handled inside get_weather for simplicity

if __name__ == "__main__":
    main()