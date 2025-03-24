"""
password_generator.py

Generates secure random passwords with configurable length and character types.

Functions:
    validate_password_length(length: int) -> bool
    generate_password(length: int, use_uppercase: bool = True, use_lowercase: bool = True,
                     use_numbers: bool = True, use_special: bool = True) -> str
    get_user_preferences() -> tuple

Command Line Usage Examples:
    python password_generator.py
    python password_generator.py --length 16
    python password_generator.py --length 12 --no-special
"""

import random
import string
import logging
import argparse
from typing import Tuple

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
        length (int): Desired password length

    Returns:
        bool: True if length is valid, False otherwise
    """
    logger.debug(f"Validating password length: {length}")
    
    try:
        if not isinstance(length, int):
            logger.error("Password length must be an integer")
            return False
        
        if length < 8:
            logger.error("Password length must be at least 8 characters")
            return False
            
        if length > 128:
            logger.error("Password length must not exceed 128 characters")
            return False
            
        return True
    except Exception as e:
        logger.error(f"Error validating password length: {e}")
        return False

def generate_password(length: int, use_uppercase: bool = True, use_lowercase: bool = True,
                     use_numbers: bool = True, use_special: bool = True) -> str:
    """
    Generates a random password with specified characteristics.

    Parameters:
        length (int): Length of the password
        use_uppercase (bool): Include uppercase letters
        use_lowercase (bool): Include lowercase letters
        use_numbers (bool): Include numbers
        use_special (bool): Include special characters

    Returns:
        str: Generated password
    """
    logger.debug(f"Generating password with length: {length} | "
                f"uppercase: {use_uppercase} | lowercase: {use_lowercase} | "
                f"numbers: {use_numbers} | special: {use_special}")

    try:
        # Initialize character pools
        chars = ''
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_numbers:
            chars += string.digits
        if use_special:
            chars += string.punctuation

        if not chars:
            logger.error("No character sets selected")
            raise ValueError("At least one character set must be selected")

        # Ensure at least one character from each selected type
        password = []
        if use_lowercase:
            password.append(random.choice(string.ascii_lowercase))
        if use_uppercase:
            password.append(random.choice(string.ascii_uppercase))
        if use_numbers:
            password.append(random.choice(string.digits))
        if use_special:
            password.append(random.choice(string.punctuation))

        # Fill the rest of the password
        remaining_length = length - len(password)
        password.extend(random.choice(chars) for _ in range(remaining_length))

        # Shuffle the password
        random.shuffle(password)
        final_password = ''.join(password)

        logger.debug(f"Password generated successfully, length: {len(final_password)}")
        return final_password

    except Exception as e:
        logger.error(f"Error generating password: {e}")
        raise

def get_user_preferences() -> Tuple[int, bool, bool, bool, bool]:
    """
    Gets password preferences from user input.

    Parameters:
        None

    Returns:
        tuple: (length, use_uppercase, use_lowercase, use_numbers, use_special)
    """
    logger.debug("Getting user preferences")
    
    try:
        while True:
            try:
                length = int(input("Enter password length (8-128): "))
                if validate_password_length(length):
                    break
            except ValueError:
                logger.error("Please enter a valid number")
                print("Please enter a valid number")

        use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
        use_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
        use_numbers = input("Include numbers? (y/n): ").lower() == 'y'
        use_special = input("Include special characters? (y/n): ").lower() == 'y'

        if not any([use_uppercase, use_lowercase, use_numbers, use_special]):
            logger.error("At least one character set must be selected")
            raise ValueError("At least one character set must be selected")

        logger.debug(f"User preferences collected successfully")
        return length, use_uppercase, use_lowercase, use_numbers, use_special

    except Exception as e:
        logger.error(f"Error getting user preferences: {e}")
        raise

def main():
    """
    Main function to run the password generator.

    Parameters:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Generate a secure random password")
    parser.add_argument("--length", type=int, default=12, help="Password length (default: 12)")
    parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase letters")
    parser.add_argument("--no-lower", action="store_true", help="Exclude lowercase letters")
    parser.add_argument("--no-numbers", action="store_true", help="Exclude numbers")
    parser.add_argument("--no-special", action="store_true", help="Exclude special characters")
    
    args = parser.parse_args()

    try:
        while True:
            print("\nPassword Generator")
            print("-----------------")

            if args.length:
                if not validate_password_length(args.length):
                    args.length = 12  # Reset to default if invalid

                password = generate_password(
                    args.length,
                    not args.no_upper,
                    not args.no_lower,
                    not args.no_numbers,
                    not args.no_special
                )
            else:
                length, use_upper, use_lower, use_numbers, use_special = get_user_preferences()
                password = generate_password(length, use_upper, use_lower, use_numbers, use_special)

            print(f"\nGenerated Password: {password}")
            
            if input("\nGenerate another password? (y/n): ").lower() != 'y':
                break

    except Exception as e:
        logger.error(f"Error in main function: {e}")
        print(f"An error occurred: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())