#!/usr/bin/env python3
import argparse
import sys

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin"""
    return celsius + 273.15

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9

def fahrenheit_to_kelvin(fahrenheit):
    """Convert Fahrenheit to Kelvin"""
    celsius = fahrenheit_to_celsius(fahrenheit)
    return celsius_to_kelvin(celsius)

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius"""
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit"""
    celsius = kelvin_to_celsius(kelvin)
    return celsius_to_fahrenheit(celsius)

def validate_temperature(value, unit):
    """Validate temperature input"""
    if unit == 'K' and value < 0:
        raise ValueError("Kelvin temperature cannot be negative")
    if unit == 'C' and value < -273.15:
        raise ValueError("Temperature cannot be below absolute zero (-273.15°C)")
    if unit == 'F' and value < -459.67:
        raise ValueError("Temperature cannot be below absolute zero (-459.67°F)")

def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between units"""
    # Validate input temperature
    validate_temperature(value, from_unit)
    
    # Convert to Celsius first (if not already in Celsius)
    if from_unit == 'F':
        celsius = fahrenheit_to_celsius(value)
    elif from_unit == 'K':
        celsius = kelvin_to_celsius(value)
    else:
        celsius = value

    # Convert from Celsius to target unit
    if to_unit == 'C':
        return celsius
    elif to_unit == 'F':
        return celsius_to_fahrenheit(celsius)
    else:
        return celsius_to_kelvin(celsius)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Convert temperatures between Celsius, Fahrenheit, and Kelvin'
    )
    
    parser.add_argument(
        'temperature',
        type=float,
        help='Temperature value to convert'
    )
    
    parser.add_argument(
        'from_unit',
        type=str,
        choices=['C', 'F', 'K'],
        help='Input temperature unit (C, F, or K)'
    )
    
    parser.add_argument(
        'to_unit',
        type=str,
        choices=['C', 'F', 'K'],
        help='Output temperature unit (C, F, or K)'
    )

    # Parse arguments
    args = parser.parse_args()

    try:
        # Perform conversion
        result = convert_temperature(
            args.temperature,
            args.from_unit,
            args.to_unit
        )
        
        # Format output with 2 decimal places
        print(f"{args.temperature}°{args.from_unit} = {result:.2f}°{args.to_unit}")
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()