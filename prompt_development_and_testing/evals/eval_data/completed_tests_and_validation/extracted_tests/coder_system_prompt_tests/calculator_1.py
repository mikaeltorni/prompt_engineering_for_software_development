"""
calculator.py

A comprehensive terminal-based calculator with basic and advanced mathematical operations.

Functions:
    display_menu(): Displays the calculator menu
    get_number(prompt): Gets and validates numerical input
    perform_basic_operation(operation, x, y): Performs basic mathematical operations
    perform_advanced_operation(operation, x): Performs advanced mathematical operations
    main(): Main calculator loop

Command Line Usage Example:
    python calculator.py
"""

import math
import logging
from typing import Union, Optional, Tuple
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

# Global variable to store calculation history
calculation_history = []

def display_menu() -> None:
    """
    Displays the calculator menu options.

    Parameters:
        None

    Returns:
        None
    """
    print("\n=== Calculator Menu ===")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Power (^)")
    print("6. Square Root (√)")
    print("7. Factorial (!)")
    print("8. View History")
    print("9. Clear History")
    print("0. Exit")
    print("====================")

def get_number(prompt: str) -> Optional[float]:
    """
    Gets and validates numerical input from the user.

    Parameters:
        prompt (str): The input prompt to display to the user

    Returns:
        Optional[float]: The validated number or None if invalid
    """
    logger.debug(f"Prompting user with: {prompt}")
    
    try:
        number = float(input(prompt))
        logger.debug(f"Received valid number: {number}")
        return number
    except ValueError:
        logger.error("Invalid number input")
        print("Error: Please enter a valid number.")
        return None

def perform_basic_operation(operation: str, x: float, y: float) -> Optional[float]:
    """
    Performs basic mathematical operations.

    Parameters:
        operation (str): The mathematical operation to perform
        x (float): First number
        y (float): Second number

    Returns:
        Optional[float]: Result of the operation or None if error
    """
    logger.debug(f"Operation: {operation} | x: {x} | y: {y}")
    
    try:
        if operation == '+':
            result = x + y
        elif operation == '-':
            result = x - y
        elif operation == '*':
            result = x * y
        elif operation == '/':
            if y == 0:
                raise ZeroDivisionError("Division by zero")
            result = x / y
        elif operation == '^':
            result = math.pow(x, y)
        else:
            logger.error(f"Invalid operation: {operation}")
            return None
            
        logger.debug(f"Result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in operation: {str(e)}")
        print(f"Error: {str(e)}")
        return None

def perform_advanced_operation(operation: str, x: float) -> Optional[float]:
    """
    Performs advanced mathematical operations.

    Parameters:
        operation (str): The mathematical operation to perform
        x (float): Number to perform operation on

    Returns:
        Optional[float]: Result of the operation or None if error
    """
    logger.debug(f"Operation: {operation} | x: {x}")
    
    try:
        if operation == 'sqrt':
            if x < 0:
                raise ValueError("Cannot calculate square root of negative number")
            result = math.sqrt(x)
        elif operation == 'factorial':
            if x < 0 or not x.is_integer():
                raise ValueError("Factorial only works with positive integers")
            result = math.factorial(int(x))
        else:
            logger.error(f"Invalid operation: {operation}")
            return None
            
        logger.debug(f"Result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in operation: {str(e)}")
        print(f"Error: {str(e)}")
        return None

def add_to_history(operation: str, result: float) -> None:
    """
    Adds an operation to the calculation history.

    Parameters:
        operation (str): The operation performed
        result (float): The result of the operation

    Returns:
        None
    """
    calculation_history.append(f"{operation} = {result}")
    logger.debug(f"Added to history: {operation} = {result}")

def main() -> None:
    """
    Main calculator loop.

    Parameters:
        None

    Returns:
        None
    """
    while True:
        display_menu()
        choice = input("Enter your choice (0-9): ")
        logger.debug(f"User choice: {choice}")

        if choice == '0':
            print("Thank you for using the calculator!")
            sys.exit(0)

        elif choice == '8':
            print("\n=== Calculation History ===")
            if not calculation_history:
                print("No calculations performed yet.")
            else:
                for i, calc in enumerate(calculation_history, 1):
                    print(f"{i}. {calc}")
            continue

        elif choice == '9':
            calculation_history.clear()
            print("History cleared.")
            continue

        elif choice in {'1', '2', '3', '4', '5'}:
            x = get_number("Enter first number: ")
            if x is None:
                continue
            
            y = get_number("Enter second number: ")
            if y is None:
                continue

            operation_map = {
                '1': ('+', 'Addition'),
                '2': ('-', 'Subtraction'),
                '3': ('*', 'Multiplication'),
                '4': ('/', 'Division'),
                '5': ('^', 'Power')
            }
            
            op_symbol, op_name = operation_map[choice]
            result = perform_basic_operation(op_symbol, x, y)
            
            if result is not None:
                print(f"\nResult: {result}")
                add_to_history(f"{x} {op_symbol} {y}", result)

        elif choice in {'6', '7'}:
            x = get_number("Enter number: ")
            if x is None:
                continue

            if choice == '6':
                result = perform_advanced_operation('sqrt', x)
                if result is not None:
                    print(f"\nResult: {result}")
                    add_to_history(f"√{x}", result)
            else:
                result = perform_advanced_operation('factorial', x)
                if result is not None:
                    print(f"\nResult: {result}")
                    add_to_history(f"{x}!", result)

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCalculator terminated by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)