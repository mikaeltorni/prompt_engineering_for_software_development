"""
weather_info.py

Fetches and displays current weather information for a given city using OpenWeatherMap API.

Functions:
    get_weather_data(city: str, api_key: str) -> dict: Fetches weather data from API
    display_weather_info(weather_data: dict) -> None: Displays formatted weather information
    validate_city_name(city: str) -> bool: Validates city name input
    main() -> None: Main program loop

Command Line Usage Example:
    python weather_info.py
"""

import requests
import json
import logging
import os
from typing import Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

def validate_city_name(city: str) -> bool:
    """
    Validates if the city name contains only letters and spaces.

    Parameters:
        city (str): City name to validate

    Returns:
        bool: True if valid, False otherwise
    """
    logger.debug(f"Validating city name: {city}")
    
    if not city:
        return False
    
    # Check if city name contains only letters and spaces
    is_valid = all(char.isalpha() or char.isspace() for char in city)
    
    logger.debug(f"City name validation result: {is_valid}")
    return is_valid

def get_weather_data(city: str, api_key: str) -> Optional[Dict]:
    """
    Fetches weather data from OpenWeatherMap API.

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
        logger.debug("Successfully fetched weather data")
        return weather_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return None

def display_weather_info(weather_data: Dict) -> None:
    """
    Displays formatted weather information.

    Parameters:
        weather_data (dict): Weather data from API

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
        
        print("\nCurrent Weather Information:")
        print("============================")
        print(f"Location: {city}, {country}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Conditions: {conditions.capitalize()}")
        print("============================\n")
        
        logger.debug("Weather information displayed successfully")
        
    except KeyError as e:
        logger.error(f"Error parsing weather data: {e}")
        print("Error: Unable to parse weather information")

def main() -> None:
    """
    Main program loop.

    Parameters:
        None

    Returns:
        None
    """
    # You would typically get this from environment variables
    API_KEY = "your_api_key_here"  # Replace with actual API key
    
    print("Welcome to Weather Information System!")
    print("Enter 'quit' to exit the program.")
    
    while True:
        city = input("\nEnter city name: ").strip()
        
        if city.lower() == 'quit':
            logger.info("User requested to quit")
            print("Goodbye!")
            break
            
        if not validate_city_name(city):
            logger.warning(f"Invalid city name entered: {city}")
            print("Please enter a valid city name (letters and spaces only).")
            continue
            
        weather_data = get_weather_data(city, API_KEY)
        
        if weather_data:
            display_weather_info(weather_data)
        else:
            print("Error: Unable to fetch weather data. Please check the city name and try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Program terminated by user")
        print("\nProgram terminated by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print("\nAn unexpected error occurred")