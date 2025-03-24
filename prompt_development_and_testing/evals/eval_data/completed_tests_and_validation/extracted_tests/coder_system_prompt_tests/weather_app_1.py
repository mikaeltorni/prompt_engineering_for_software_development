"""
weather_info.py

Fetches and displays current weather information for a given city using OpenWeatherMap API.

Functions:
    get_weather(city: str, api_key: str) -> dict: Fetches weather data for a given city
    display_weather(weather_data: dict) -> None: Displays formatted weather information
    validate_city(city: str) -> bool: Validates city name input
    get_api_key() -> str: Gets API key from user

Command Line Usage Example:
    python weather_info.py
"""

import requests
import json
import sys
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

def validate_city(city: str) -> bool:
    """
    Validates if the city name contains only letters and spaces.

    Parameters:
        city (str): Name of the city to validate

    Returns:
        bool: True if valid, False otherwise
    """
    logger.debug(f"Validating city name: {city}")
    
    if not city:
        return False
    
    # Check if city contains only letters and spaces
    is_valid = all(char.isalpha() or char.isspace() for char in city)
    
    logger.debug(f"City validation result: {is_valid}")
    return is_valid

def get_api_key() -> str:
    """
    Gets API key from user input.

    Parameters:
        None

    Returns:
        str: API key
    """
    api_key = input("Please enter your OpenWeatherMap API key: ").strip()
    logger.debug("API key received")
    return api_key

def get_weather(city: str, api_key: str) -> Optional[Dict]:
    """
    Fetches weather data for the specified city.

    Parameters:
        city (str): Name of the city
        api_key (str): OpenWeatherMap API key

    Returns:
        dict: Weather data if successful, None if failed
    """
    logger.debug(f"Fetching weather data for city: {city}")
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        # Make API request
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'  # Use metric units
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        
        weather_data = response.json()
        logger.debug("Weather data successfully retrieved")
        return weather_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return None

def display_weather(weather_data: Dict) -> None:
    """
    Displays formatted weather information.

    Parameters:
        weather_data (dict): Weather data to display

    Returns:
        None
    """
    logger.debug("Displaying weather information")
    
    try:
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        conditions = weather_data['weather'][0]['description']
        city_name = weather_data['name']
        country = weather_data['sys']['country']

        print("\n=== Weather Information ===")
        print(f"Location: {city_name}, {country}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Conditions: {conditions.capitalize()}")
        print("========================\n")
        
        logger.debug("Weather information displayed successfully")
        
    except KeyError as e:
        logger.error(f"Error parsing weather data: {e}")
        print("Error: Unable to parse weather data")

def main():
    """
    Main program loop.

    Parameters:
        None

    Returns:
        None
    """
    print("Welcome to Weather Information Program!")
    api_key = get_api_key()

    while True:
        city = input("\nEnter city name (or 'quit' to exit): ").strip()
        
        if city.lower() == 'quit':
            print("Thank you for using Weather Information Program!")
            sys.exit(0)
            
        if not validate_city(city):
            print("Error: Please enter a valid city name (letters and spaces only)")
            continue
            
        weather_data = get_weather(city, api_key)
        
        if weather_data:
            display_weather(weather_data)
        else:
            print("Error: Unable to fetch weather data. Please check the city name and try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print("An unexpected error occurred")
        sys.exit(1)