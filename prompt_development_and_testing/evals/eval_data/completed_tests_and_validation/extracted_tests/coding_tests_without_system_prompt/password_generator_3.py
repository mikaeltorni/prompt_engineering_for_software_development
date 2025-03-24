import random
import string

def generate_password(length=12, use_uppercase=True, use_lowercase=True, 
                     use_numbers=True, use_special=True):
    """
    Generate a random password based on specified criteria.
    
    Parameters:
    length (int): Length of the password
    use_uppercase (bool): Include uppercase letters
    use_lowercase (bool): Include lowercase letters
    use_numbers (bool): Include numbers
    use_special (bool): Include special characters
    
    Returns:
    str: Generated password
    """
    
    # Initialize an empty character pool
    char_pool = ''
    
    # Add character sets based on user preferences
    if use_uppercase:
        char_pool += string.ascii_uppercase
    if use_lowercase:
        char_pool += string.ascii_lowercase
    if use_numbers:
        char_pool += string.digits
    if use_special:
        char_pool += string.punctuation
    
    # Check if at least one character set is selected
    if not char_pool:
        raise ValueError("At least one character set must be selected!")
    
    # Generate password
    password = []
    
    # Ensure at least one character from each selected set is included
    if use_uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if use_lowercase:
        password.append(random.choice(string.ascii_lowercase))
    if use_numbers:
        password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice(string.punctuation))
    
    # Fill the remaining length with random characters
    remaining_length = length - len(password)
    password.extend(random.choice(char_pool) for _ in range(remaining_length))
    
    # Shuffle the password
    random.shuffle(password)
    
    # Convert list to string and return
    return ''.join(password)

def get_user_input():
    """Get password requirements from user."""
    print("\nPassword Generator")
    print("-----------------")
    
    while True:
        try:
            length = int(input("\nEnter password length (minimum 4): "))
            if length < 4:
                print("Password length must be at least 4 characters!")
                continue
            break
        except ValueError:
            print("Please enter a valid number!")
    
    uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
    numbers = input("Include numbers? (y/n): ").lower() == 'y'
    special = input("Include special characters? (y/n): ").lower() == 'y'
    
    if not any([uppercase, lowercase, numbers, special]):
        print("Error: At least one character set must be selected!")
        return get_user_input()
    
    return length, uppercase, lowercase, numbers, special

def main():
    try:
        # Get user preferences
        length, uppercase, lowercase, numbers, special = get_user_input()
        
        # Generate password
        password = generate_password(length, uppercase, lowercase, numbers, special)
        
        # Display the generated password
        print("\nGenerated Password:", password)
        print("Password length:", len(password))
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        main()
        if input("\nGenerate another password? (y/n): ").lower() != 'y':
            break
    print("\nThank you for using the Password Generator!")