"""
temperature_converter.py

A command-line tool for converting temperatures between Celsius, Fahrenheit, and Kelvin.

Functions:
    validate_temperature(temp: float, unit: str) -> bool: Validates temperature values
    celsius_to_fahrenheit(celsius: float) -> float: Converts Celsius to Fahrenheit
    celsius_to_kelvin(celsius: float) -> float: Converts Celsius to Kelvin
    fahrenheit_to_celsius(fahrenheit: float) -> float: Converts Fahrenheit to Celsius
    fahrenheit_to_kelvin(fahrenheit: float) -> float: Converts Fahrenheit to Kelvin
    kelvin_to_celsius(kelvin: float) -> float: Converts Kelvin to Celsius
    kelvin_to_fahrenheit(kelvin: float) -> float: Converts Kelvin to Fahrenheit
    convert_temperature(temp: float, from_unit: str, to_unit: str) -> float: Converts temperature between units

Command Line Usage Examples:
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

def validate_temperature(temp: float, unit: str) -> bool:
    """
    Validates if the temperature value is within valid ranges for the given unit.

    Parameters:
        temp (float): Temperature value to validate
        unit (str): Temperature unit ('C', 'F', or 'K')

    Returns:
        bool: True if temperature is valid, False otherwise
    """
    logger.debug(f"Validating temperature: {temp} {unit}")
    
    try:
        if unit.upper() == 'K' and temp < 0:
            logger.error("Temperature below absolute zero in Kelvin")
            return False
        elif unit.upper() == 'C' and temp < -273.15:
            logger.error("Temperature below absolute zero in Celsius")
            return False
        elif unit.upper() == 'F' and temp < -459.67:
            logger.error("Temperature below absolute zero in Fahrenheit")
            return False
        return True
    except Exception as e:
        logger.error(f"Validation error: {e}")
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
    return celsius + 273.15

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
    return (fahrenheit - 32) * 5/9 + 273.15

def kelvin_to_celsius(kelvin: float) -> float:
    """
    Converts Kelvin to Celsius.

    Parameters:
        kelvin (float): Temperature in Kelvin

    Returns:
        float: Temperature in Celsius
    """
    logger.debug(f"Converting {kelvin}K to Celsius")
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin: float) -> float:
    """
    Converts Kelvin to Fahrenheit.

    Parameters:
        kelvin (float): Temperature in Kelvin

    Returns:
        float: Temperature in Fahrenheit
    """
    logger.debug(f"Converting {kelvin}K to Fahrenheit")
    return (kelvin - 273.15) * 9/5 + 32

def convert_temperature(temp: float, from_unit: str, to_unit: str) -> float:
    """
    Converts temperature between different units.

    Parameters:
        temp (float): Temperature value to convert
        from_unit (str): Original temperature unit
        to_unit (str): Target temperature unit

    Returns:
        float: Converted temperature value
    """
    logger.debug(f"Converting {temp} from {from_unit} to {to_unit}")
    
    # Standardize units to uppercase
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    
    # Validate input
    if not validate_temperature(temp, from_unit):
        raise ValueError("Invalid temperature value")
    
    # Convert to target unit
    if from_unit == to_unit:
        return temp
    
    conversion_map = {
        ('C', 'F'): celsius_to_fahrenheit,
        ('C', 'K'): celsius_to_kelvin,
        ('F', 'C'): fahrenheit_to_celsius,
        ('F', 'K'): fahrenheit_to_kelvin,
        ('K', 'C'): kelvin_to_celsius,
        ('K', 'F'): kelvin_to_fahrenheit
    }
    
    converter = conversion_map.get((from_unit, to_unit))
    if converter:
        return converter(temp)
    else:
        raise ValueError("Invalid unit conversion")

def main():
    """
    Main function to run the temperature converter program.

    Parameters:
        None

    Returns:
        None
    """
    print("Temperature Converter")
    print("Enter 'q' to quit")
    
    while True:
        try:
            # Get input temperature
            temp_input = input("\nEnter temperature value: ")
            if temp_input.lower() == 'q':
                print("Goodbye!")
                sys.exit(0)
                
            temp = float(temp_input)
            
            # Get input unit
            from_unit = input("Enter input unit (C/F/K): ").upper()
            if from_unit not in ['C', 'F', 'K']:
                print("Invalid input unit. Please use C, F, or K.")
                continue
                
            # Get target unit
            to_unit = input("Enter target unit (C/F/K): ").upper()
            if to_unit not in ['C', 'F', 'K']:
                print("Invalid target unit. Please use C, F, or K.")
                continue
            
            # Perform conversion
            result = convert_temperature(temp, from_unit, to_unit)
            print(f"\nResult: {temp}°{from_unit} = {result:.2f}°{to_unit}")
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            print("Please enter a valid number for temperature.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print("An error occurred. Please try again.")

if __name__ == "__main__":
    main()