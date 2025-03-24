"""
weather_info.py

Fetches and displays current weather information for a specified city using the OpenWeatherMap API.

Functions:
    load_api_key(): Loads API key from environment variables
    get_weather_data(city: str, api_key: str): Fetches weather data from the API
    display_weather_info(weather_data: dict): Displays formatted weather information
    main(): Main program loop

Command Line Usage Example:
    python weather_info.py
"""

import requests
import json
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

def load_api_key() -> str:
    """
    Loads the OpenWeatherMap API key from environment variables.

    Parameters:
        None

    Returns:
        str: API key if found, raises error if not found
    """
    logger.debug("Loading API key from environment")
    
    load_dotenv()
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    
    if not api_key:
        logger.error("API key not found in environment variables")
        raise ValueError("API key not found. Please set OPENWEATHERMAP_API_KEY environment variable")
    
    return api_key

def get_weather_data(city: str, api_key: str) -> dict:
    """
    Fetches weather data from OpenWeatherMap API for the specified city.

    Parameters:
        city (str): Name of the city
        api_key (str): OpenWeatherMap API key

    Returns:
        dict: Weather data for the specified city
    """
    logger.debug(f"Fetching weather data for city: {city}")
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Use metric units
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        weather_data = response.json()
        logger.debug(f"Successfully retrieved weather data for {city}")
        return weather_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        raise RuntimeError(f"Failed to fetch weather data: {e}")

def display_weather_info(weather_data: dict) -> None:
    """
    Displays formatted weather information.

    Parameters:
        weather_data (dict): Weather data from the API

    Returns:
        None
    """
    logger.debug("Displaying weather information")
    
    try:
        city = weather_data['name']
        country = weather_data['sys']['country']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        conditions = weather_data['weather'][0]['description']
        feels_like = weather_data['main']['feels_like']

        print("\nCurrent Weather Information:")
        print("=" * 30)
        print(f"Location: {city}, {country}")
        print(f"Temperature: {temp}°C")
        print(f"Feels Like: {feels_like}°C")
        print(f"Humidity: {humidity}%")
        print(f"Conditions: {conditions.capitalize()}")
        print("=" * 30)
        
    except KeyError as e:
        logger.error(f"Error parsing weather data: {e}")
        raise ValueError(f"Invalid weather data format: missing {e}")

def main() -> None:
    """
    Main program loop.

    Parameters:
        None

    Returns:
        None
    """
    logger.debug("Starting weather information program")
    
    try:
        api_key = load_api_key()
        
        while True:
            print("\nWeather Information Program")
            print("Enter 'quit' to exit")
            
            city = input("\nEnter city name: ").strip()
            
            if city.lower() == 'quit':
                logger.info("User requested to quit")
                break
                
            if not city:
                logger.warning("Empty city name provided")
                print("Please enter a valid city name.")
                continue
                
            try:
                weather_data = get_weather_data(city, api_key)
                display_weather_info(weather_data)
                
            except (RuntimeError, ValueError) as e:
                print(f"Error: {e}")
                logger.error(f"Error processing request: {e}")
                
            except Exception as e:
                print("An unexpected error occurred. Please try again.")
                logger.error(f"Unexpected error: {e}")
                
    except Exception as e:
        logger.error(f"Critical error in main program: {e}")
        print("A critical error occurred. Please check the logs.")
        
    finally:
        logger.debug("Program terminated")

if __name__ == "__main__":
    main()