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
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

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
    print("===================")

def get_number(prompt: str) -> float:
    """
    Gets and validates numerical input from the user.

    Parameters:
        prompt (str): The input prompt to display to the user

    Returns:
        float: The validated number
    """
    logger.debug(f"Prompting user with: {prompt}")
    while True:
        try:
            num = float(input(prompt))
            logger.debug(f"Received input: {num}")
            return num
        except ValueError:
            logger.error("Invalid number input")
            print("Invalid input. Please enter a valid number.")

def perform_basic_operation(operation: str, x: float, y: float) -> float:
    """
    Performs basic mathematical operations.

    Parameters:
        operation (str): The operation to perform (+, -, *, /)
        x (float): First number
        y (float): Second number

    Returns:
        float: Result of the operation
    """
    logger.debug(f"Operation: {operation} | x: {x} | y: {y}")
    
    try:
        if operation == '+':
            return x + y
        elif operation == '-':
            return x - y
        elif operation == '*':
            return x * y
        elif operation == '/':
            if y == 0:
                raise ValueError("Division by zero")
            return x / y
        else:
            raise ValueError("Invalid operation")
    except Exception as e:
        logger.error(f"Error in basic operation: {e}")
        raise

def perform_advanced_operation(operation: str, x: float) -> float:
    """
    Performs advanced mathematical operations.

    Parameters:
        operation (str): The operation to perform (sqrt, factorial)
        x (float): Number to perform operation on

    Returns:
        float: Result of the operation
    """
    logger.debug(f"Operation: {operation} | x: {x}")
    
    try:
        if operation == 'sqrt':
            if x < 0:
                raise ValueError("Cannot calculate square root of negative number")
            return math.sqrt(x)
        elif operation == 'factorial':
            if x < 0 or not x.is_integer():
                raise ValueError("Factorial only works with non-negative integers")
            return math.factorial(int(x))
        else:
            raise ValueError("Invalid operation")
    except Exception as e:
        logger.error(f"Error in advanced operation: {e}")
        raise

def main() -> None:
    """
    Main calculator loop.

    Parameters:
        None

    Returns:
        None
    """
    history = []
    
    while True:
        try:
            display_menu()
            choice = input("Enter your choice (0-9): ")
            logger.debug(f"User choice: {choice}")

            if choice == '0':
                logger.info("Exiting calculator")
                print("Thank you for using the calculator!")
                sys.exit(0)

            elif choice == '8':  # View History
                print("\n=== Operation History ===")
                for entry in history:
                    print(entry)
                continue

            elif choice == '9':  # Clear History
                history.clear()
                print("History cleared!")
                continue

            elif choice in {'1', '2', '3', '4', '5'}:
                x = get_number("Enter first number: ")
                y = get_number("Enter second number: ")
                
                operations = {
                    '1': ('+', lambda: perform_basic_operation('+', x, y)),
                    '2': ('-', lambda: perform_basic_operation('-', x, y)),
                    '3': ('*', lambda: perform_basic_operation('*', x, y)),
                    '4': ('/', lambda: perform_basic_operation('/', x, y)),
                    '5': ('^', lambda: math.pow(x, y))
                }
                
                op_symbol, operation = operations[choice]
                result = operation()
                expression = f"{x} {op_symbol} {y} = {result}"

            elif choice in {'6', '7'}:
                x = get_number("Enter number: ")
                
                if choice == '6':
                    result = perform_advanced_operation('sqrt', x)
                    expression = f"√{x} = {result}"
                else:
                    result = perform_advanced_operation('factorial', x)
                    expression = f"{x}! = {result}"

            else:
                print("Invalid choice! Please try again.")
                continue

            print(f"\nResult: {result}")
            history.append(expression)
            logger.info(f"Calculation performed: {expression}")

        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            print(f"Error: {ve}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()