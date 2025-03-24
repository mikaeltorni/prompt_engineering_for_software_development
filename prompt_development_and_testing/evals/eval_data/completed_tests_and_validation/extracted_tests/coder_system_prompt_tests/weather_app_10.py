"""
weather_info.py

Fetches and displays current weather information for a given city using the OpenWeatherMap API.

Functions:
    validate_api_key(api_key: str) -> bool
    validate_city_name(city: str) -> bool
    fetch_weather_data(city: str, api_key: str) -> dict
    display_weather_info(weather_data: dict) -> None
    main() -> None

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

def validate_api_key(api_key: str) -> bool:
    """
    Validates the API key format.

    Parameters:
        api_key (str): The API key to validate

    Returns:
        bool: True if valid, False otherwise
    """
    logger.debug(f"Validating API key length: {len(api_key)}")
    
    if not api_key or len(api_key) < 32:
        logger.error("Invalid API key format")
        return False
    return True

def validate_city_name(city: str) -> bool:
    """
    Validates the city name format.

    Parameters:
        city (str): The city name to validate

    Returns:
        bool: True if valid, False otherwise
    """
    logger.debug(f"Validating city name: {city}")
    
    if not city or not city.replace(" ", "").isalpha():
        logger.error("Invalid city name format")
        return False
    return True

def fetch_weather_data(city: str, api_key: str) -> Dict:
    """
    Fetches weather data from OpenWeatherMap API.

    Parameters:
        city (str): The city name to get weather for
        api_key (str): The API key for authentication

    Returns:
        dict: Weather data if successful
    """
    logger.debug(f"Fetching weather data for city: {city}")
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'  # For Celsius
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        weather_data = response.json()
        logger.debug("Weather data successfully fetched")
        return weather_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        raise

def display_weather_info(weather_data: Dict) -> None:
    """
    Displays weather information in a formatted way.

    Parameters:
        weather_data (dict): Weather data to display

    Returns:
        None
    """
    logger.debug("Displaying weather information")
    
    try:
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        city_name = weather_data['name']
        
        print("\nCurrent Weather Information:")
        print("=" * 30)
        print(f"City: {city_name}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Conditions: {description.capitalize()}")
        print("=" * 30)
        
    except KeyError as e:
        logger.error(f"Error parsing weather data: {e}")
        print("Error: Unable to parse weather information")

def main() -> None:
    """
    Main function to run the weather information program.

    Parameters:
        None

    Returns:
        None
    """
    print("Welcome to Weather Information System!")
    
    # Get API key
    api_key = input("Please enter your OpenWeatherMap API key: ").strip()
    if not validate_api_key(api_key):
        logger.error("Invalid API key provided")
        print("Error: Invalid API key")
        sys.exit(1)

    while True:
        print("\nOptions:")
        print("1. Get weather information")
        print("2. Exit")
        
        choice = input("Enter your choice (1-2): ").strip()
        
        if choice == "2":
            print("Thank you for using Weather Information System!")
            break
            
        elif choice == "1":
            city = input("Enter city name: ").strip()
            
            if not validate_city_name(city):
                print("Error: Invalid city name")
                continue
                
            try:
                weather_data = fetch_weather_data(city, api_key)
                display_weather_info(weather_data)
                
            except requests.exceptions.RequestException as e:
                print(f"Error: Unable to fetch weather data. Please check your internet connection and try again.")
                logger.error(f"Request failed: {e}")
                
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                logger.error(f"Unexpected error: {e}")
                
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)