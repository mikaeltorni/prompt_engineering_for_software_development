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
            return f"Error fetching weather data: {str(e)}"
        except json.JSONDecodeError:
            return "Error parsing weather data"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    def format_weather_data(self, weather_data):
        # Extract relevant information
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather_condition = weather_data['weather'][0]['description']
        feels_like = weather_data['main']['feels_like']
        wind_speed = weather_data['wind']['speed']
        city_name = weather_data['name']
        country = weather_data['sys']['country']
        sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')

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
    weather_app = WeatherApp()
    
    while True:
        print("\nWeather Information Service")
        print("---------------------------")
        city = input("Enter city name (or 'quit' to exit): ").strip()
        
        if city.lower() == 'quit':
            print("Thank you for using the Weather Information Service!")
            break
            
        if city:
            print("\nFetching weather data...")
            weather_info = weather_app.get_weather(city)
            print(weather_info)
        else:
            print("Please enter a valid city name.")

if __name__ == "__main__":
    main()