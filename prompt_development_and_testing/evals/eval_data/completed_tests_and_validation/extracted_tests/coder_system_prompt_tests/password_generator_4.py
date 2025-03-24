"""
password_generator.py

Generates secure random passwords with configurable length and character sets.

Functions:
    generate_password(length: int, use_uppercase: bool = True, use_lowercase: bool = True,
                     use_numbers: bool = True, use_special: bool = True) -> str
    validate_password_length(length: int) -> None
    get_character_set(use_uppercase: bool, use_lowercase: bool,
                     use_numbers: bool, use_special: bool) -> str

Command Line Usage Examples:
    python password_generator.py
    python password_generator.py --length 16
    python password_generator.py --length 12 --no-special
"""

import random
import string
import argparse
import logging
import sys
from typing import NoReturn

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

def validate_password_length(length: int) -> None:
    """
    Validates the password length parameter.

    Parameters:
        length (int): The desired password length

    Returns:
        None

    Raises:
        ValueError: If length is less than 8 or greater than 128
    """
    logger.debug(f"Validating password length: {length}")
    
    if not isinstance(length, int):
        raise TypeError("Password length must be an integer")
    if length < 8:
        raise ValueError("Password length must be at least 8 characters")
    if length > 128:
        raise ValueError("Password length must not exceed 128 characters")

def get_character_set(use_uppercase: bool, use_lowercase: bool,
                     use_numbers: bool, use_special: bool) -> str:
    """
    Creates a character set based on selected options.

    Parameters:
        use_uppercase (bool): Include uppercase letters
        use_lowercase (bool): Include lowercase letters
        use_numbers (bool): Include numbers
        use_special (bool): Include special characters

    Returns:
        str: String containing all allowed characters
    """
    logger.debug(f"Creating character set with uppercase: {use_uppercase}, "
                f"lowercase: {use_lowercase}, numbers: {use_numbers}, "
                f"special: {use_special}")

    if not any([use_uppercase, use_lowercase, use_numbers, use_special]):
        raise ValueError("At least one character set must be selected")

    chars = ''
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_numbers:
        chars += string.digits
    if use_special:
        chars += string.punctuation

    return chars

def generate_password(length: int, use_uppercase: bool = True,
                     use_lowercase: bool = True, use_numbers: bool = True,
                     use_special: bool = True) -> str:
    """
    Generates a random password with the specified parameters.

    Parameters:
        length (int): Length of the password
        use_uppercase (bool): Include uppercase letters
        use_lowercase (bool): Include lowercase letters
        use_numbers (bool): Include numbers
        use_special (bool): Include special characters

    Returns:
        str: Generated password
    """
    logger.debug(f"Generating password with length: {length}")

    try:
        validate_password_length(length)
        chars = get_character_set(use_uppercase, use_lowercase,
                                use_numbers, use_special)
        
        # Generate password
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Ensure at least one character from each selected set is included
        if use_uppercase and not any(c.isupper() for c in password):
            password = random.choice(string.ascii_uppercase) + password[1:]
        if use_lowercase and not any(c.islower() for c in password):
            password = password[:-1] + random.choice(string.ascii_lowercase)
        if use_numbers and not any(c.isdigit() for c in password):
            password = password[len(password)//2:] + random.choice(string.digits) + password[:len(password)//2]
        if use_special and not any(c in string.punctuation for c in password):
            insert_pos = random.randint(1, len(password)-2)
            password = password[:insert_pos] + random.choice(string.punctuation) + password[insert_pos+1:]

        logger.debug("Password generated successfully")
        return password

    except (ValueError, TypeError) as e:
        logger.error(f"Error generating password: {str(e)}")
        raise

def main() -> NoReturn:
    """
    Main function to run the password generator.

    Parameters:
        None

    Returns:
        NoReturn
    """
    parser = argparse.ArgumentParser(description='Generate a secure random password')
    parser.add_argument('--length', type=int, default=12,
                      help='Length of the password (default: 12)')
    parser.add_argument('--no-uppercase', action='store_false',
                      dest='use_uppercase', help='Exclude uppercase letters')
    parser.add_argument('--no-lowercase', action='store_false',
                      dest='use_lowercase', help='Exclude lowercase letters')
    parser.add_argument('--no-numbers', action='store_false',
                      dest='use_numbers', help='Exclude numbers')
    parser.add_argument('--no-special', action='store_false',
                      dest='use_special', help='Exclude special characters')

    args = parser.parse_args()

    while True:
        try:
            password = generate_password(
                args.length,
                args.use_uppercase,
                args.use_lowercase,
                args.use_numbers,
                args.use_special
            )
            print("\nGenerated Password:", password)
            
            choice = input("\nGenerate another password? (y/n): ").lower()
            if choice != 'y':
                print("Goodbye!")
                break

        except (ValueError, TypeError) as e:
            logger.error(f"Error: {str(e)}")
            print(f"Error: {str(e)}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            print(f"An unexpected error occurred: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    main()