"""
calculator.py

A comprehensive terminal-based calculator with basic and advanced mathematical operations.

Functions:
    get_number(): Gets and validates numerical input from user
    perform_basic_operation(operation, num1, num2): Performs basic mathematical operations
    perform_advanced_operation(operation, num): Performs advanced mathematical operations
    display_menu(): Displays the calculator menu
    main(): Main program loop

Command Line Usage Example:
    python calculator.py
"""

import math
import logging
from typing import Union, Tuple

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

def get_number(prompt: str) -> float:
    """
    Gets and validates numerical input from user.
    
    Parameters:
        prompt (str): The input prompt to display to user
        
    Returns:
        float: The validated number
    """
    while True:
        try:
            number = float(input(prompt))
            logger.debug(f"Input received: {number}")
            return number
        except ValueError:
            logger.error("Invalid number input")
            print("Please enter a valid number.")

def perform_basic_operation(operation: str, num1: float, num2: float) -> Union[float, str]:
    """
    Performs basic mathematical operations.
    
    Parameters:
        operation (str): The operation to perform (+, -, *, /)
        num1 (float): First number
        num2 (float): Second number
        
    Returns:
        Union[float, str]: Result of the operation or error message
    """
    logger.debug(f"Operation: {operation} | num1: {num1} | num2: {num2}")
    
    try:
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            if num2 == 0:
                raise ZeroDivisionError("Division by zero")
            return num1 / num2
    except Exception as e:
        logger.error(f"Error in basic operation: {e}")
        return f"Error: {str(e)}"

def perform_advanced_operation(operation: str, num: float) -> Union[float, str]:
    """
    Performs advanced mathematical operations.
    
    Parameters:
        operation (str): The operation to perform (sqrt, factorial, etc.)
        num (float): The number to perform operation on
        
    Returns:
        Union[float, str]: Result of the operation or error message
    """
    logger.debug(f"Operation: {operation} | num: {num}")
    
    try:
        if operation == 'sqrt':
            if num < 0:
                raise ValueError("Cannot calculate square root of negative number")
            return math.sqrt(num)
        elif operation == 'factorial':
            if num < 0 or not num.is_integer():
                raise ValueError("Factorial only works with positive integers")
            return math.factorial(int(num))
        elif operation == 'sin':
            return math.sin(math.radians(num))
        elif operation == 'cos':
            return math.cos(math.radians(num))
        elif operation == 'tan':
            return math.tan(math.radians(num))
    except Exception as e:
        logger.error(f"Error in advanced operation: {e}")
        return f"Error: {str(e)}"

def display_menu() -> None:
    """
    Displays the calculator menu.
    
    Parameters:
        None
        
    Returns:
        None
    """
    print("\n=== Calculator Menu ===")
    print("Basic Operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("\nAdvanced Operations:")
    print("5. Square Root (sqrt)")
    print("6. Factorial (!)")
    print("7. Sine (sin)")
    print("8. Cosine (cos)")
    print("9. Tangent (tan)")
    print("0. Exit")
    print("===================")

def main() -> None:
    """
    Main program loop.
    
    Parameters:
        None
        
    Returns:
        None
    """
    logger.info("Starting calculator")
    
    while True:
        display_menu()
        choice = input("Enter your choice (0-9): ")
        logger.debug(f"User choice: {choice}")
        
        if choice == '0':
            logger.info("Exiting calculator")
            print("Thank you for using the calculator!")
            break
            
        if choice in ['1', '2', '3', '4']:
            num1 = get_number("Enter first number: ")
            num2 = get_number("Enter second number: ")
            
            operations = {
                '1': ('+', perform_basic_operation),
                '2': ('-', perform_basic_operation),
                '3': ('*', perform_basic_operation),
                '4': ('/', perform_basic_operation)
            }
            
            op, func = operations[choice]
            result = func(op, num1, num2)
            
        elif choice in ['5', '6', '7', '8', '9']:
            num = get_number("Enter number: ")
            
            operations = {
                '5': ('sqrt', perform_advanced_operation),
                '6': ('factorial', perform_advanced_operation),
                '7': ('sin', perform_advanced_operation),
                '8': ('cos', perform_advanced_operation),
                '9': ('tan', perform_advanced_operation)
            }
            
            op, func = operations[choice]
            result = func(op, num)
            
        else:
            logger.warning("Invalid choice selected")
            print("Invalid choice! Please select a number between 0 and 9.")
            continue
            
        print(f"\nResult: {result}")
        logger.info(f"Calculation result: {result}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Calculator terminated by user")
        print("\nCalculator terminated by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\nAn unexpected error occurred: {e}")