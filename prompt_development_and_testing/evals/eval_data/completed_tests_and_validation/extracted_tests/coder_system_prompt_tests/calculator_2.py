"""
calculator.py

A comprehensive terminal-based calculator with basic and advanced mathematical operations.

Functions:
    get_number(): Gets and validates numerical input from user
    basic_operation(operation, x, y): Performs basic mathematical operations
    advanced_operation(operation, x): Performs advanced mathematical operations
    display_menu(): Displays the calculator menu
    display_history(history): Displays calculation history
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

def basic_operation(operation, x, y):
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
    except Exception as e:
        logger.error(f"Error in basic operation: {e}")
        raise

def advanced_operation(operation, x):
    """
    Performs advanced mathematical operations.
    
    Parameters:
        operation (str): The operation to perform (sqrt, factorial, etc.)
        x (float): The number to operate on
        
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
                raise ValueError("Factorial only works with positive integers")
            return math.factorial(int(x))
        elif operation == 'sin':
            return math.sin(math.radians(x))
        elif operation == 'cos':
            return math.cos(math.radians(x))
        elif operation == 'tan':
            return math.tan(math.radians(x))
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
    print("\nCalculator Menu:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Square Root (√)")
    print("6. Factorial (!)")
    print("7. Sine (sin)")
    print("8. Cosine (cos)")
    print("9. Tangent (tan)")
    print("10. View History")
    print("11. Exit")

def display_history(history):
    """
    Displays calculation history.
    
    Parameters:
        history (list): List of calculation history
        
    Returns:
        None
    """
    print("\nCalculation History:")
    for i, entry in enumerate(history, 1):
        print(f"{i}. {entry}")

def main():
    """
    Main calculator loop.
    
    Parameters:
        None
        
    Returns:
        None
    """
    history = []
    operations = {
        '1': '+', '2': '-', '3': '*', '4': '/',
        '5': 'sqrt', '6': 'factorial',
        '7': 'sin', '8': 'cos', '9': 'tan'
    }

    while True:
        try:
            display_menu()
            choice = input("\nEnter your choice (1-11): ")
            logger.debug(f"User choice: {choice}")

            if choice == '11':
                print("Thank you for using the calculator!")
                sys.exit(0)

            if choice == '10':
                display_history(history)
                continue

            if choice not in operations:
                print("Invalid choice. Please try again.")
                continue

            operation = operations[choice]
            
            # Basic operations (require two numbers)
            if choice in ['1', '2', '3', '4']:
                x = get_number("Enter first number: ")
                y = get_number("Enter second number: ")
                try:
                    result = basic_operation(operation, x, y)
                    expression = f"{x} {operation} {y} = {result}"
                except ValueError as e:
                    print(f"Error: {e}")
                    continue

            # Advanced operations (require one number)
            else:
                x = get_number()
                try:
                    result = advanced_operation(operation, x)
                    expression = f"{operation}({x}) = {result}"
                except ValueError as e:
                    print(f"Error: {e}")
                    continue

            print(f"\nResult: {result}")
            history.append(expression)
            logger.info(f"Calculation performed: {expression}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()