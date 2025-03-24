"""
temperature_converter.py

A command-line tool for converting temperatures between Celsius, Fahrenheit, and Kelvin.

Functions:
    validate_temperature(temp: float, unit: str) -> bool: Validates if temperature is within physical limits
    celsius_to_fahrenheit(celsius: float) -> float: Converts Celsius to Fahrenheit
    celsius_to_kelvin(celsius: float) -> float: Converts Celsius to Kelvin
    fahrenheit_to_celsius(fahrenheit: float) -> float: Converts Fahrenheit to Celsius
    fahrenheit_to_kelvin(fahrenheit: float) -> float: Converts Fahrenheit to Kelvin
    kelvin_to_celsius(kelvin: float) -> float: Converts Kelvin to Celsius
    kelvin_to_fahrenheit(kelvin: float) -> float: Converts Kelvin to Fahrenheit
    convert_temperature(temp: float, from_unit: str, to_unit: str) -> float: Converts temperature between units
    get_user_input() -> tuple: Gets and validates user input
    main() -> None: Main program loop

Command Line Usage Example:
    python temperature_converter.py
"""

import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

# Constants for absolute zero in different units
ABSOLUTE_ZERO_C = -273.15
ABSOLUTE_ZERO_F = -459.67
ABSOLUTE_ZERO_K = 0

def validate_temperature(temp: float, unit: str) -> bool:
    """
    Validates if the temperature is physically possible (above absolute zero).

    Parameters:
        temp (float): Temperature value to validate
        unit (str): Temperature unit ('C', 'F', or 'K')

    Returns:
        bool: True if temperature is valid, False otherwise
    """
    logger.debug(f"Validating temperature: {temp}{unit}")
    
    if unit.upper() == 'C':
        return temp >= ABSOLUTE_ZERO_C
    elif unit.upper() == 'F':
        return temp >= ABSOLUTE_ZERO_F
    elif unit.upper() == 'K':
        return temp >= ABSOLUTE_ZERO_K
    return False

def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Converts Celsius to Fahrenheit.

    Parameters:
        celsius (float): Temperature in Celsius

    Returns:
        float: Temperature in Fahrenheit
    """
    logger.debug(f"Converting {celsius}°C to Fahrenheit")
    return (celsius * 9/5) + 32

def celsius_to_kelvin(celsius: float) -> float:
    """
    Converts Celsius to Kelvin.

    Parameters:
        celsius (float): Temperature in Celsius

    Returns:
        float: Temperature in Kelvin
    """
    logger.debug(f"Converting {celsius}°C to Kelvin")
    return celsius - ABSOLUTE_ZERO_C

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Converts Fahrenheit to Celsius.

    Parameters:
        fahrenheit (float): Temperature in Fahrenheit

    Returns:
        float: Temperature in Celsius
    """
    logger.debug(f"Converting {fahrenheit}°F to Celsius")
    return (fahrenheit - 32) * 5/9

def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """
    Converts Fahrenheit to Kelvin.

    Parameters:
        fahrenheit (float): Temperature in Fahrenheit

    Returns:
        float: Temperature in Kelvin
    """
    logger.debug(f"Converting {fahrenheit}°F to Kelvin")
    return (fahrenheit - 32) * 5/9 - ABSOLUTE_ZERO_C

def kelvin_to_celsius(kelvin: float) -> float:
    """
    Converts Kelvin to Celsius.

    Parameters:
        kelvin (float): Temperature in Kelvin

    Returns:
        float: Temperature in Celsius
    """
    logger.debug(f"Converting {kelvin}K to Celsius")
    return kelvin + ABSOLUTE_ZERO_C

def kelvin_to_fahrenheit(kelvin: float) -> float:
    """
    Converts Kelvin to Fahrenheit.

    Parameters:
        kelvin (float): Temperature in Kelvin

    Returns:
        float: Temperature in Fahrenheit
    """
    logger.debug(f"Converting {kelvin}K to Fahrenheit")
    return (kelvin + ABSOLUTE_ZERO_C) * 9/5 + 32

def convert_temperature(temp: float, from_unit: str, to_unit: str) -> float:
    """
    Converts temperature between units.

    Parameters:
        temp (float): Temperature value to convert
        from_unit (str): Original temperature unit
        to_unit (str): Target temperature unit

    Returns:
        float: Converted temperature value
    """
    logger.debug(f"Converting {temp}{from_unit} to {to_unit}")
    
    # Standardize units to uppercase
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    
    # If units are the same, return original temperature
    if from_unit == to_unit:
        return temp
    
    # Convert to target unit
    if from_unit == 'C':
        if to_unit == 'F':
            return celsius_to_fahrenheit(temp)
        elif to_unit == 'K':
            return celsius_to_kelvin(temp)
    elif from_unit == 'F':
        if to_unit == 'C':
            return fahrenheit_to_celsius(temp)
        elif to_unit == 'K':
            return fahrenheit_to_kelvin(temp)
    elif from_unit == 'K':
        if to_unit == 'C':
            return kelvin_to_celsius(temp)
        elif to_unit == 'F':
            return kelvin_to_fahrenheit(temp)
    
    raise ValueError("Invalid unit conversion")

def get_user_input() -> tuple:
    """
    Gets and validates user input for temperature conversion.

    Parameters:
        None

    Returns:
        tuple: (temperature, from_unit, to_unit) or (None, None, None) if user wants to quit
    """
    try:
        # Get temperature value
        temp_input = input("\nEnter temperature value (or 'q' to quit): ")
        if temp_input.lower() == 'q':
            return None, None, None
        
        temp = float(temp_input)
        
        # Get input unit
        from_unit = input("Enter input unit (C/F/K): ").upper()
        if from_unit not in ['C', 'F', 'K']:
            logger.error("Invalid input unit")
            raise ValueError("Invalid input unit. Use C, F, or K.")
        
        # Validate temperature
        if not validate_temperature(temp, from_unit):
            logger.error(f"Temperature below absolute zero: {temp}{from_unit}")
            raise ValueError(f"Temperature cannot be below absolute zero")
        
        # Get target unit
        to_unit = input("Enter target unit (C/F/K): ").upper()
        if to_unit not in ['C', 'F', 'K']:
            logger.error("Invalid target unit")
            raise ValueError("Invalid target unit. Use C, F, or K.")
        
        return temp, from_unit, to_unit
        
    except ValueError as e:
        logger.error(f"Input error: {e}")
        return None, None, None

def main() -> None:
    """
    Main program loop.

    Parameters:
        None

    Returns:
        None
    """
    print("Welcome to Temperature Converter!")
    print("--------------------------------")
    
    while True:
        temp, from_unit, to_unit = get_user_input()
        
        if temp is None:
            if from_unit is None and to_unit is None:
                print("\nGoodbye!")
                break
            print("\nInvalid input. Please try again.")
            continue
            
        try:
            result = convert_temperature(temp, from_unit, to_unit)
            print(f"\nResult: {temp}{from_unit} = {result:.2f}{to_unit}")
        except Exception as e:
            logger.error(f"Conversion error: {e}")
            print(f"Error during conversion: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)