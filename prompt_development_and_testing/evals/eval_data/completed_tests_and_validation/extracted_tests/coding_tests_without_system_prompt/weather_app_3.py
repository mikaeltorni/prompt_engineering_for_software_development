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
        if not self.api_key:
            raise ValueError("API key not found. Please set OPENWEATHER_API_KEY in .env file")
        
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        """
        Fetch weather data for the specified city
        """
        try:
            # Build the API request URL
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # Use metric units (Celsius)
            }

            # Make the API request
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Parse the JSON response
            weather_data = response.json()
            
            return self.format_weather_data(weather_data)
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}"
        except json.JSONDecodeError:
            return "Error parsing weather data"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    def format_weather_data(self, data):
        """
        Format the weather data for display
        """
        # Extract relevant information
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        weather_desc = data['weather'][0]['description']
        feels_like = data['main']['feels_like']
        wind_speed = data['wind']['speed']
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')

        # Create formatted output
        output = f"""
Weather Information for {data['name']}, {data['sys']['country']}
═══════════════════════════════════════════════
Temperature: {temperature}°C
Feels like: {feels_like}°C
Humidity: {humidity}%
Conditions: {weather_desc.capitalize()}
Wind Speed: {wind_speed} m/s
Sunrise: {sunrise}
Sunset: {sunset}
═══════════════════════════════════════════════
        """
        return output

def main():
    # Create WeatherApp instance
    weather_app = WeatherApp()

    while True:
        # Get city input from user
        print("\nEnter a city name (or 'quit' to exit):")
        city = input("> ").strip()

        if city.lower() == 'quit':
            print("Goodbye!")
            break

        if not city:
            print("Please enter a valid city name.")
            continue

        # Get and display weather information
        weather_info = weather_app.get_weather(city)
        print(weather_info)

if __name__ == "__main__":
    main()