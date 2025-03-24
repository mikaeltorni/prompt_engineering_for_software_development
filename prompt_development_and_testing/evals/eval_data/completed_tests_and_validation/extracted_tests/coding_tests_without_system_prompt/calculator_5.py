def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Cannot divide by zero"
    return x / y

def power(x, y):
    return x ** y

def modulus(x, y):
    if y == 0:
        return "Error: Cannot divide by zero"
    return x % y

def calculator():
    print("\n=== Simple Calculator ===")
    print("Operations available:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Power (**)")
    print("6. Modulus (%)")
    print("7. Exit")

    while True:
        try:
            # Get operation choice from user
            choice = input("\nEnter operation number (1-7): ")

            # Exit condition
            if choice == '7':
                print("Thank you for using the calculator!")
                break

            # Check if choice is valid
            if choice not in ['1', '2', '3', '4', '5', '6']:
                print("Invalid operation number! Please try again.")
                continue

            # Get numbers from user
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            # Perform calculation based on operation choice
            if choice == '1':
                print(f"\n{num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"\n{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"\n{num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                result = divide(num1, num2)
                print(f"\n{num1} / {num2} = {result}")
            elif choice == '5':
                print(f"\n{num1} ** {num2} = {power(num1, num2)}")
            elif choice == '6':
                result = modulus(num1, num2)
                print(f"\n{num1} % {num2} = {result}")

        except ValueError:
            print("Invalid input! Please enter numeric values.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    calculator()