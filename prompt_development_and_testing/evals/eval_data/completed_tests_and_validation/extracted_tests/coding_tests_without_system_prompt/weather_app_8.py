import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherApp:
    def __init__(self):
        # Get API key from environment variables
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        try:
            # Create parameters for the API request
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # Use metric units (Celsius)
            }

            # Make the API request
            response = requests.get(self.base_url, params=params)
            
            # Check if the request was successful
            if response.status_code == 200:
                weather_data = response.json()
                return self.format_weather_data(weather_data)
            else:
                return f"Error: Unable to fetch weather data. Status code: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

    def format_weather_data(self, data):
        # Extract relevant information from the API response
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        weather_condition = data['weather'][0]['description']
        feels_like = data['main']['feels_like']
        wind_speed = data['wind']['speed']
        city_name = data['name']
        country = data['sys']['country']
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')

        # Format the weather information
        weather_info = f"""
╔══════════════════════════════════════════════
║ Weather in {city_name}, {country}
╠══════════════════════════════════════════════
║ Temperature: {temperature}°C
║ Feels like: {feels_like}°C
║ Humidity: {humidity}%
║ Conditions: {weather_condition.capitalize()}
║ Wind Speed: {wind_speed} m/s
║ Sunrise: {sunrise}
║ Sunset: {sunset}
╚══════════════════════════════════════════════
"""
        return weather_info

def main():
    # Create an instance of WeatherApp
    weather_app = WeatherApp()

    while True:
        # Get city input from user
        city = input("\nEnter city name (or 'quit' to exit): ").strip()
        
        if city.lower() == 'quit':
            print("Goodbye!")
            break

        if city:
            # Get and display weather information
            weather_info = weather_app.get_weather(city)
            print(weather_info)
        else:
            print("Please enter a valid city name.")

if __name__ == "__main__":
    # Print welcome message
    print("Welcome to the Weather Information App!")
    print("======================================")
    main()