"""
advanced_calculator.py

A terminal-based calculator with basic and advanced mathematical operations.

Functions:
    get_number(): Gets and validates numerical input from user
    perform_basic_operation(operation, num1, num2): Performs basic mathematical operations
    perform_advanced_operation(operation, num): Performs advanced mathematical operations
    display_menu(): Displays the calculator menu
    main(): Main program loop

Command Line Usage Example:
    python advanced_calculator.py
"""

import math
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

# Global variable to store calculation history
calculation_history = []

def get_number(prompt="Enter a number: "):
    """
    Gets and validates numerical input from user.

    Parameters:
        prompt (str): The input prompt to display

    Returns:
        float: The validated number
    """
    while True:
        try:
            number = float(input(prompt))
            logger.debug(f"Input number: {number}")
            return number
        except ValueError:
            logger.error("Invalid number input")
            print("Please enter a valid number.")

def perform_basic_operation(operation, num1, num2):
    """
    Performs basic mathematical operations.

    Parameters:
        operation (str): The operation to perform (+, -, *, /)
        num1 (float): First number
        num2 (float): Second number

    Returns:
        float: Result of the operation
    """
    logger.debug(f"Operation: {operation} | num1: {num1} | num2: {num2}")
    
    try:
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                raise ValueError("Division by zero is not allowed")
            result = num1 / num2
        else:
            raise ValueError("Invalid operation")

        calculation_history.append(f"{num1} {operation} {num2} = {result}")
        logger.debug(f"Result: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in basic operation: {e}")
        raise

def perform_advanced_operation(operation, num):
    """
    Performs advanced mathematical operations.

    Parameters:
        operation (str): The operation to perform (sqrt, factorial, etc.)
        num (float): The number to operate on

    Returns:
        float: Result of the operation
    """
    logger.debug(f"Advanced operation: {operation} | num: {num}")
    
    try:
        if operation == 'sqrt':
            if num < 0:
                raise ValueError("Cannot calculate square root of negative number")
            result = math.sqrt(num)
        elif operation == 'factorial':
            if num < 0 or not num.is_integer():
                raise ValueError("Factorial only works with positive integers")
            result = math.factorial(int(num))
        elif operation == 'sin':
            result = math.sin(math.radians(num))
        elif operation == 'cos':
            result = math.cos(math.radians(num))
        else:
            raise ValueError("Invalid operation")

        calculation_history.append(f"{operation}({num}) = {result}")
        logger.debug(f"Result: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in advanced operation: {e}")
        raise

def display_menu():
    """
    Displays the calculator menu.

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
    print("5. Square Root (√)")
    print("6. Factorial (!)")
    print("7. Sine (sin)")
    print("8. Cosine (cos)")
    print("9. View History")
    print("0. Exit")
    print("====================")

def main():
    """
    Main program loop.

    Parameters:
        None

    Returns:
        None
    """
    logger.info("Starting calculator")
    
    while True:
        try:
            display_menu()
            choice = input("Enter your choice (0-9): ")
            logger.debug(f"User choice: {choice}")

            if choice == '0':
                print("Thank you for using the calculator!")
                sys.exit(0)

            if choice == '9':
                print("\n=== Calculation History ===")
                for item in calculation_history:
                    print(item)
                continue

            if choice in {'1', '2', '3', '4'}:
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                
                operation_map = {
                    '1': '+',
                    '2': '-',
                    '3': '*',
                    '4': '/'
                }
                
                result = perform_basic_operation(operation_map[choice], num1, num2)
                print(f"Result: {result}")

            elif choice in {'5', '6', '7', '8'}:
                num = get_number("Enter number: ")
                
                operation_map = {
                    '5': 'sqrt',
                    '6': 'factorial',
                    '7': 'sin',
                    '8': 'cos'
                }
                
                result = perform_advanced_operation(operation_map[choice], num)
                print(f"Result: {result}")

            else:
                print("Invalid choice! Please select a number between 0 and 9.")

        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            print(f"Error: {ve}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()