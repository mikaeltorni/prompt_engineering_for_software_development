"""
calculator.py

A terminal-based calculator that performs various mathematical operations.

Functions:
    display_menu(): Displays the calculator menu
    get_number(prompt): Gets and validates numerical input
    perform_operation(operation, num1, num2): Performs the selected mathematical operation
    main(): Main program loop

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
    Displays the calculator's menu of available operations.

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
    print("8. Exit")
    print("====================")

def get_number(prompt: str) -> float:
    """
    Gets and validates numerical input from the user.

    Parameters:
        prompt (str): The input prompt to display to the user

    Returns:
        float: The validated numerical input
    """
    while True:
        try:
            logger.debug(f"Requesting input with prompt: {prompt}")
            num = float(input(prompt))
            logger.debug(f"Received input: {num}")
            return num
        except ValueError:
            logger.error("Invalid numerical input")
            print("Invalid input. Please enter a valid number.")

def perform_operation(operation: str, num1: float, num2: float = None) -> float:
    """
    Performs the selected mathematical operation.

    Parameters:
        operation (str): The operation to perform
        num1 (float): First number
        num2 (float): Second number (optional, defaults to None)

    Returns:
        float: Result of the operation
    """
    logger.debug(f"Operation: {operation} | num1: {num1} | num2: {num2}")

    try:
        if operation == '1':  # Addition
            return num1 + num2
        elif operation == '2':  # Subtraction
            return num1 - num2
        elif operation == '3':  # Multiplication
            return num1 * num2
        elif operation == '4':  # Division
            if num2 == 0:
                raise ValueError("Division by zero is not allowed")
            return num1 / num2
        elif operation == '5':  # Power
            return math.pow(num1, num2)
        elif operation == '6':  # Square Root
            if num1 < 0:
                raise ValueError("Cannot calculate square root of a negative number")
            return math.sqrt(num1)
        elif operation == '7':  # Factorial
            if num1 < 0 or num1 != int(num1):
                raise ValueError("Factorial is only defined for non-negative integers")
            return math.factorial(int(num1))
        else:
            raise ValueError("Invalid operation")

    except Exception as e:
        logger.error(f"Error in calculation: {str(e)}")
        raise

def main() -> None:
    """
    Main program loop for the calculator.

    Parameters:
        None

    Returns:
        None
    """
    logger.info("Starting calculator")
    
    while True:
        try:
            display_menu()
            operation = input("Enter your choice (1-8): ")
            logger.debug(f"Selected operation: {operation}")

            if operation == '8':
                logger.info("Exiting calculator")
                print("Thank you for using the calculator!")
                sys.exit(0)

            # Operations that need two numbers
            if operation in ['1', '2', '3', '4', '5']:
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                result = perform_operation(operation, num1, num2)

            # Operations that need one number
            elif operation in ['6', '7']:
                num1 = get_number("Enter the number: ")
                result = perform_operation(operation, num1)

            else:
                logger.error(f"Invalid operation selected: {operation}")
                print("Invalid operation. Please select a valid option (1-8).")
                continue

            logger.info(f"Calculation result: {result}")
            print(f"\nResult: {result}")

        except ValueError as ve:
            logger.error(f"ValueError: {str(ve)}")
            print(f"Error: {str(ve)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            print(f"An unexpected error occurred: {str(e)}")

        # Ask if user wants to continue
        continue_calc = input("\nDo you want to perform another calculation? (y/n): ").lower()
        if continue_calc != 'y':
            logger.info("Exiting calculator")
            print("Thank you for using the calculator!")
            break

if __name__ == "__main__":
    main()