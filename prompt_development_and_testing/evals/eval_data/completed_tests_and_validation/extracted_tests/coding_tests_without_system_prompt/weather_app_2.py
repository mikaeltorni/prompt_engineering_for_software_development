import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherApp:
    def __init__(self):
        # Get API key from environment variable
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

    def format_weather_data(self, data):
        # Extract relevant information
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
{'='*50}
Weather Information for {city_name}, {country}
{'='*50}

Temperature: {temperature}°C
Feels like: {feels_like}°C
Humidity: {humidity}%
Weather Condition: {weather_condition.capitalize()}
Wind Speed: {wind_speed} m/s
Sunrise: {sunrise}
Sunset: {sunset}
{'='*50}
"""
        return weather_info

def main():
    weather_app = WeatherApp()
    
    while True:
        print("\nWeather Information Service")
        print("1. Get weather information")
        print("2. Exit")
        
        choice = input("Enter your choice (1-2): ")
        
        if choice == '1':
            city = input("\nEnter city name: ")
            print("\nFetching weather information...")
            weather_info = weather_app.get_weather(city)
            print(weather_info)
        elif choice == '2':
            print("\nThank you for using the Weather Information Service!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()