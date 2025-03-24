"""
password_generator.py

Generates secure random passwords with configurable length and character types.

Functions:
    generate_password(length: int) -> str: Generates a random password
    validate_password_length(length: int) -> bool: Validates the password length
    get_user_input() -> int: Gets and validates user input for password length

Command Line Usage Examples:
    python password_generator.py
    python password_generator.py --length 16
"""

import random
import string
import logging
import argparse
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

def validate_password_length(length: int) -> bool:
    """
    Validates if the password length is within acceptable range.
    
    Parameters:
        length (int): The desired password length
        
    Returns:
        bool: True if length is valid, False otherwise
    """
    logger.debug(f"Validating password length: {length}")
    
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    
    if not isinstance(length, int):
        logger.error("Password length must be an integer")
        return False
    
    if length < MIN_LENGTH:
        logger.error(f"Password length must be at least {MIN_LENGTH} characters")
        return False
    
    if length > MAX_LENGTH:
        logger.error(f"Password length must not exceed {MAX_LENGTH} characters")
        return False
    
    return True

def generate_password(length: int) -> str:
    """
    Generates a random password with specified length.
    
    Parameters:
        length (int): The desired length of the password
        
    Returns:
        str: Generated password
        
    Raises:
        ValueError: If length is invalid
    """
    logger.debug(f"Generating password with length: {length}")
    
    if not validate_password_length(length):
        raise ValueError("Invalid password length")
    
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character from each set
    password: List[str] = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    # Fill the rest of the password
    all_chars = lowercase + uppercase + digits + special_chars
    for _ in range(length - len(password)):
        password.append(random.choice(all_chars))
    
    # Shuffle the password
    random.shuffle(password)
    final_password = ''.join(password)
    
    logger.debug("Password generated successfully")
    return final_password

def get_user_input() -> int:
    """
    Gets and validates password length from user input.
    
    Parameters:
        None
        
    Returns:
        int: Validated password length
    """
    while True:
        try:
            length = input("Enter desired password length (minimum 8): ")
            length = int(length)
            
            if validate_password_length(length):
                return length
                
        except ValueError:
            logger.error("Please enter a valid number")

def main():
    """
    Main function to run the password generator.
    
    Parameters:
        None
        
    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Generate a secure random password")
    parser.add_argument("--length", type=int, help="Length of the password")
    args = parser.parse_args()
    
    try:
        while True:
            if args.length:
                length = args.length
            else:
                length = get_user_input()
            
            password = generate_password(length)
            print(f"\nGenerated Password: {password}")
            
            if args.length:  # If length was provided as command-line argument, exit after one password
                break
                
            another = input("\nGenerate another password? (y/n): ").lower()
            if another != 'y':
                break
                
    except KeyboardInterrupt:
        logger.info("Password generator terminated by user")
        print("\nExiting password generator")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print("\nAn error occurred while generating the password")

if __name__ == "__main__":
    main()