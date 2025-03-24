"""
contact_book.py

A simple contact book application that manages contacts through terminal interface.
Contacts are stored in a JSON file.

Classes:
    Contact: Represents a single contact
    ContactBook: Manages the collection of contacts

Functions:
    display_menu(): Displays the main menu
    get_valid_input(prompt, validator): Gets validated input from user

Command Line Usage Example:
    python contact_book.py
"""

import json
from pathlib import Path
import logging
from typing import Dict, List, Optional, Callable
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

class Contact:
    """
    Represents a single contact with name, phone, and email.
    """
    def __init__(self, name: str, phone: str, email: str):
        """
        Initialize a new contact.

        Parameters:
            name (str): Contact's name
            phone (str): Contact's phone number
            email (str): Contact's email address

        Returns:
            None
        """
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self) -> Dict:
        """
        Convert contact to dictionary format.

        Parameters:
            None

        Returns:
            Dict: Dictionary representation of the contact
        """
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Contact':
        """
        Create a Contact instance from a dictionary.

        Parameters:
            data (Dict): Dictionary containing contact information

        Returns:
            Contact: New Contact instance
        """
        return cls(data["name"], data["phone"], data["email"])

class ContactBook:
    """
    Manages a collection of contacts with save/load functionality.
    """
    def __init__(self, filename: str = "contacts.json"):
        """
        Initialize the contact book.

        Parameters:
            filename (str): Name of the file to store contacts

        Returns:
            None
        """
        self.filename = Path(filename)
        self.contacts: List[Contact] = []
        self.load_contacts()

    def load_contacts(self) -> None:
        """
        Load contacts from JSON file.

        Parameters:
            None

        Returns:
            None
        """
        logger.debug(f"Loading contacts from {self.filename}")
        if self.filename.exists():
            try:
                with self.filename.open('r') as f:
                    data = json.load(f)
                    self.contacts = [Contact.from_dict(contact) for contact in data]
                logger.info(f"Loaded {len(self.contacts)} contacts")
            except json.JSONDecodeError as e:
                logger.error(f"Error loading contacts: {e}")
                self.contacts = []
        else:
            logger.info("No existing contacts file found")
            self.contacts = []

    def save_contacts(self) -> None:
        """
        Save contacts to JSON file.

        Parameters:
            None

        Returns:
            None
        """
        logger.debug("Saving contacts")
        try:
            with self.filename.open('w') as f:
                json.dump([contact.to_dict() for contact in self.contacts], f, indent=2)
            logger.info(f"Saved {len(self.contacts)} contacts")
        except Exception as e:
            logger.error(f"Error saving contacts: {e}")

    def add_contact(self, contact: Contact) -> None:
        """
        Add a new contact to the book.

        Parameters:
            contact (Contact): Contact to add

        Returns:
            None
        """
        logger.debug(f"Adding contact: {contact.name}")
        self.contacts.append(contact)
        self.save_contacts()

    def search_contacts(self, term: str) -> List[Contact]:
        """
        Search contacts by name.

        Parameters:
            term (str): Search term

        Returns:
            List[Contact]: List of matching contacts
        """
        logger.debug(f"Searching for: {term}")
        return [contact for contact in self.contacts 
                if term.lower() in contact.name.lower()]

    def update_contact(self, old_name: str, new_contact: Contact) -> bool:
        """
        Update an existing contact.

        Parameters:
            old_name (str): Name of contact to update
            new_contact (Contact): Updated contact information

        Returns:
            bool: True if update successful, False otherwise
        """
        logger.debug(f"Updating contact: {old_name}")
        for i, contact in enumerate(self.contacts):
            if contact.name.lower() == old_name.lower():
                self.contacts[i] = new_contact
                self.save_contacts()
                return True
        return False

    def delete_contact(self, name: str) -> bool:
        """
        Delete a contact by name.

        Parameters:
            name (str): Name of contact to delete

        Returns:
            bool: True if deletion successful, False otherwise
        """
        logger.debug(f"Deleting contact: {name}")
        initial_length = len(self.contacts)
        self.contacts = [contact for contact in self.contacts 
                        if contact.name.lower() != name.lower()]
        if len(self.contacts) < initial_length:
            self.save_contacts()
            return True
        return False

def get_valid_input(prompt: str, validator: Callable[[str], bool]) -> str:
    """
    Get validated input from user.

    Parameters:
        prompt (str): Input prompt
        validator (Callable[[str], bool]): Validation function

    Returns:
        str: Validated input
    """
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print("Invalid input. Please try again.")

def display_menu() -> None:
    """
    Display the main menu.

    Parameters:
        None

    Returns:
        None
    """
    print("\n=== Contact Book Menu ===")
    print("1. Add Contact")
    print("2. Search Contacts")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Exit")

def main():
    """
    Main program loop.

    Parameters:
        None

    Returns:
        None
    """
    contact_book = ContactBook()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            # Add Contact
            name = get_valid_input("Enter name: ", lambda x: len(x) > 0)
            phone = get_valid_input("Enter phone: ", lambda x: x.isdigit())
            email = get_valid_input("Enter email: ", lambda x: "@" in x)
            contact_book.add_contact(Contact(name, phone, email))
            print("Contact added successfully!")

        elif choice == "2":
            # Search Contacts
            term = input("Enter search term: ")
            results = contact_book.search_contacts(term)
            if results:
                print("\nSearch results:")
                for contact in results:
                    print(f"\nName: {contact.name}")
                    print(f"Phone: {contact.phone}")
                    print(f"Email: {contact.email}")
            else:
                print("No contacts found.")

        elif choice == "3":
            # Update Contact
            old_name = input("Enter name of contact to update: ")
            name = get_valid_input("Enter new name: ", lambda x: len(x) > 0)
            phone = get_valid_input("Enter new phone: ", lambda x: x.isdigit())
            email = get_valid_input("Enter new email: ", lambda x: "@" in x)
            if contact_book.update_contact(old_name, Contact(name, phone, email)):
                print("Contact updated successfully!")
            else:
                print("Contact not found.")

        elif choice == "4":
            # Delete Contact
            name = input("Enter name of contact to delete: ")
            if contact_book.delete_contact(name):
                print("Contact deleted successfully!")
            else:
                print("Contact not found.")

        elif choice == "5":
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()