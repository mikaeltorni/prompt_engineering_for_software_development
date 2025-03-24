"""
contact_book.py

A simple contact management system that stores contacts in a JSON file.

Classes:
    Contact: Represents a single contact
    ContactBook: Manages the collection of contacts

Functions:
    main(): Main program loop

Command Line Usage Example:
    python contact_book.py
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

class Contact:
    """
    Represents a single contact with name, phone, email, and address.
    """
    def __init__(self, name: str, phone: str, email: str, address: str):
        """
        Initialize a new contact.

        Parameters:
            name (str): Contact's name
            phone (str): Contact's phone number
            email (str): Contact's email address
            address (str): Contact's physical address

        Returns:
            None
        """
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

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
            "email": self.email,
            "address": self.address
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
        return cls(
            name=data["name"],
            phone=data["phone"],
            email=data["email"],
            address=data["address"]
        )

class ContactBook:
    """
    Manages a collection of contacts with operations for adding, searching,
    updating, and deleting contacts.
    """
    def __init__(self, filename: str = "contacts.json"):
        """
        Initialize the contact book.

        Parameters:
            filename (str): Name of the JSON file to store contacts

        Returns:
            None
        """
        self.filename = filename
        self.contacts: List[Contact] = []
        self.load_contacts()

    def load_contacts(self) -> None:
        """
        Load contacts from the JSON file.

        Parameters:
            None

        Returns:
            None
        """
        logger.debug(f"Loading contacts from {self.filename}")
        path = Path(self.filename)
        if path.exists():
            try:
                with path.open('r') as f:
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
        Save contacts to the JSON file.

        Parameters:
            None

        Returns:
            None
        """
        logger.debug("Saving contacts")
        try:
            with open(self.filename, 'w') as f:
                json.dump([contact.to_dict() for contact in self.contacts], f, indent=2)
            logger.info(f"Saved {len(self.contacts)} contacts")
        except Exception as e:
            logger.error(f"Error saving contacts: {e}")
            raise

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
        Search for contacts by name or phone number.

        Parameters:
            term (str): Search term

        Returns:
            List[Contact]: List of matching contacts
        """
        logger.debug(f"Searching for: {term}")
        term = term.lower()
        return [
            contact for contact in self.contacts
            if term in contact.name.lower() or term in contact.phone
        ]

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
        self.contacts = [c for c in self.contacts if c.name.lower() != name.lower()]
        if len(self.contacts) < initial_length:
            self.save_contacts()
            return True
        return False

def get_valid_input(prompt: str, allow_empty: bool = False) -> str:
    """
    Get valid input from user.

    Parameters:
        prompt (str): Prompt to display to user
        allow_empty (bool): Whether to allow empty input

    Returns:
        str: Valid user input
    """
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("This field cannot be empty. Please try again.")

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
        print("\nContact Book Menu:")
        print("1. Add Contact")
        print("2. Search Contacts")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. List All Contacts")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            name = get_valid_input("Enter name: ")
            phone = get_valid_input("Enter phone: ")
            email = get_valid_input("Enter email: ")
            address = get_valid_input("Enter address: ")
            contact_book.add_contact(Contact(name, phone, email, address))
            print("Contact added successfully!")

        elif choice == "2":
            term = get_valid_input("Enter search term: ")
            results = contact_book.search_contacts(term)
            if results:
                print("\nSearch results:")
                for contact in results:
                    print(f"\nName: {contact.name}")
                    print(f"Phone: {contact.phone}")
                    print(f"Email: {contact.email}")
                    print(f"Address: {contact.address}")
            else:
                print("No contacts found.")

        elif choice == "3":
            old_name = get_valid_input("Enter name of contact to update: ")
            name = get_valid_input("Enter new name: ")
            phone = get_valid_input("Enter new phone: ")
            email = get_valid_input("Enter new email: ")
            address = get_valid_input("Enter new address: ")
            if contact_book.update_contact(old_name, Contact(name, phone, email, address)):
                print("Contact updated successfully!")
            else:
                print("Contact not found.")

        elif choice == "4":
            name = get_valid_input("Enter name of contact to delete: ")
            if contact_book.delete_contact(name):
                print("Contact deleted successfully!")
            else:
                print("Contact not found.")

        elif choice == "5":
            if contact_book.contacts:
                print("\nAll Contacts:")
                for contact in contact_book.contacts:
                    print(f"\nName: {contact.name}")
                    print(f"Phone: {contact.phone}")
                    print(f"Email: {contact.email}")
                    print(f"Address: {contact.address}")
            else:
                print("No contacts in the book.")

        elif choice == "6":
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)