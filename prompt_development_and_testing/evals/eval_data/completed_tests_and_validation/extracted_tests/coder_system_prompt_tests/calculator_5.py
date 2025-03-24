"""
calculator.py

A terminal-based calculator supporting basic and advanced mathematical operations.

Functions:
    get_number(): Gets and validates numerical input from user
    basic_operation(operation, x, y): Performs basic mathematical operations
    advanced_operation(operation, x): Performs advanced mathematical operations
    display_menu(): Displays the calculator menu
    calculate(): Main calculator loop

Command Line Usage Example:
    python calculator.py
"""

import math
import logging
from typing import Union, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

def get_number(prompt: str) -> Optional[float]:
    """
    Gets and validates numerical input from user.
    
    Parameters:
        prompt (str): The input prompt to display to user
        
    Returns:
        float: The validated number or None if invalid input
    """
    while True:
        try:
            logger.debug(f"Requesting input with prompt: {prompt}")
            num = float(input(prompt))
            logger.debug(f"Received input: {num}")
            return num
        except ValueError:
            logger.error("Invalid number input")
            print("Please enter a valid number.")
            return None

def basic_operation(operation: str, x: float, y: float) -> Optional[float]:
    """
    Performs basic mathematical operations.
    
    Parameters:
        operation (str): The operation to perform (+, -, *, /)
        x (float): First number
        y (float): Second number
        
    Returns:
        float: Result of the operation or None if error
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
                raise ZeroDivisionError("Division by zero")
            return x / y
    except Exception as e:
        logger.error(f"Error in basic operation: {e}")
        print(f"Error: {e}")
        return None

def advanced_operation(operation: str, x: float) -> Optional[float]:
    """
    Performs advanced mathematical operations.
    
    Parameters:
        operation (str): The operation to perform (sqrt, factorial, etc.)
        x (float): The number to operate on
        
    Returns:
        float: Result of the operation or None if error
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
    except Exception as e:
        logger.error(f"Error in advanced operation: {e}")
        print(f"Error: {e}")
        return None

def display_menu() -> None:
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
    print("5. Square Root (sqrt)")
    print("6. Factorial (!)")
    print("7. Sine (sin)")
    print("8. Cosine (cos)")
    print("9. Exit")

def calculate() -> None:
    """
    Main calculator loop.
    
    Parameters:
        None
        
    Returns:
        None
    """
    while True:
        display_menu()
        
        choice = input("\nEnter your choice (1-9): ")
        logger.debug(f"User choice: {choice}")
        
        if choice == '9':
            logger.info("Exiting calculator")
            print("Thank you for using the calculator!")
            break
            
        if choice in ['1', '2', '3', '4']:
            x = get_number("Enter first number: ")
            if x is None:
                continue
            y = get_number("Enter second number: ")
            if y is None:
                continue
                
            operation_map = {'1': '+', '2': '-', '3': '*', '4': '/'}
            result = basic_operation(operation_map[choice], x, y)
            
        elif choice in ['5', '6', '7', '8']:
            x = get_number("Enter number: ")
            if x is None:
                continue
                
            operation_map = {'5': 'sqrt', '6': 'factorial', '7': 'sin', '8': 'cos'}
            result = advanced_operation(operation_map[choice], x)
            
        else:
            logger.warning(f"Invalid choice: {choice}")
            print("Invalid choice! Please select a number between 1 and 9.")
            continue
            
        if result is not None:
            logger.info(f"Calculation result: {result}")
            print(f"\nResult: {result}")
        
        # Ask if user wants to continue
        continue_calc = input("\nDo you want to perform another calculation? (y/n): ").lower()
        if continue_calc != 'y':
            logger.info("User chose to exit")
            print("Thank you for using the calculator!")
            break

if __name__ == "__main__":
    print("Welcome to the Calculator!")
    calculate()