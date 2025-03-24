"""
contact_book.py

A simple contact book application that manages contacts with CRUD operations
and stores them in a JSON file.

Functions:
    validate_phone(phone: str) -> bool
    validate_email(email: str) -> bool
    main() -> None

Command Line Usage Example:
    python contact_book.py
"""

import json
import re
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
    Represents a contact with basic information.
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

class ContactBook:
    """
    Manages a collection of contacts with CRUD operations.
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
        Load contacts from JSON file.

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
                    contacts_data = json.load(f)
                    self.contacts = [Contact(**contact) for contact in contacts_data]
                logger.info(f"Loaded {len(self.contacts)} contacts")
            except Exception as e:
                logger.error(f"Error loading contacts: {e}")
                sys.exit(1)

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
            with open(self.filename, 'w') as f:
                json.dump([contact.to_dict() for contact in self.contacts], f, indent=2)
            logger.info("Contacts saved successfully")
        except Exception as e:
            logger.error(f"Error saving contacts: {e}")

    def add_contact(self, contact: Contact) -> bool:
        """
        Add a new contact to the book.

        Parameters:
            contact (Contact): Contact object to add

        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug(f"Adding contact: {contact.name}")
        if not any(c.phone == contact.phone for c in self.contacts):
            self.contacts.append(contact)
            self.save_contacts()
            return True
        return False

    def search_contacts(self, term: str) -> List[Contact]:
        """
        Search contacts by name or phone number.

        Parameters:
            term (str): Search term

        Returns:
            List[Contact]: List of matching contacts
        """
        logger.debug(f"Searching for: {term}")
        term = term.lower()
        return [c for c in self.contacts 
                if term in c.name.lower() or term in c.phone]

    def update_contact(self, phone: str, updated_contact: Contact) -> bool:
        """
        Update an existing contact.

        Parameters:
            phone (str): Phone number of contact to update
            updated_contact (Contact): New contact information

        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug(f"Updating contact with phone: {phone}")
        for i, contact in enumerate(self.contacts):
            if contact.phone == phone:
                self.contacts[i] = updated_contact
                self.save_contacts()
                return True
        return False

    def delete_contact(self, phone: str) -> bool:
        """
        Delete a contact by phone number.

        Parameters:
            phone (str): Phone number of contact to delete

        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug(f"Deleting contact with phone: {phone}")
        for i, contact in enumerate(self.contacts):
            if contact.phone == phone:
                del self.contacts[i]
                self.save_contacts()
                return True
        return False

def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.

    Parameters:
        phone (str): Phone number to validate

    Returns:
        bool: True if valid, False otherwise
    """
    return bool(re.match(r'^\d{10}$', phone))

def validate_email(email: str) -> bool:
    """
    Validate email address format.

    Parameters:
        email (str): Email address to validate

    Returns:
        bool: True if valid, False otherwise
    """
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

def main() -> None:
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
        
        if choice == '1':
            name = input("Enter name: ")
            while True:
                phone = input("Enter phone number (10 digits): ")
                if validate_phone(phone):
                    break
                print("Invalid phone number format!")
            
            while True:
                email = input("Enter email: ")
                if validate_email(email):
                    break
                print("Invalid email format!")
            
            address = input("Enter address: ")
            
            contact = Contact(name, phone, email, address)
            if contact_book.add_contact(contact):
                print("Contact added successfully!")
            else:
                print("Contact with this phone number already exists!")

        elif choice == '2':
            term = input("Enter search term: ")
            results = contact_book.search_contacts(term)
            if results:
                print("\nSearch results:")
                for contact in results:
                    print(f"\nName: {contact.name}")
                    print(f"Phone: {contact.phone}")
                    print(f"Email: {contact.email}")
                    print(f"Address: {contact.address}")
            else:
                print("No contacts found!")

        elif choice == '3':
            phone = input("Enter phone number of contact to update: ")
            if not validate_phone(phone):
                print("Invalid phone number format!")
                continue
                
            results = contact_book.search_contacts(phone)
            if not results:
                print("Contact not found!")
                continue
                
            print("\nEnter new details:")
            name = input("Enter name: ")
            email = input("Enter email: ")
            if not validate_email(email):
                print("Invalid email format!")
                continue
            address = input("Enter address: ")
            
            updated_contact = Contact(name, phone, email, address)
            if contact_book.update_contact(phone, updated_contact):
                print("Contact updated successfully!")
            else:
                print("Update failed!")

        elif choice == '4':
            phone = input("Enter phone number of contact to delete: ")
            if contact_book.delete_contact(phone):
                print("Contact deleted successfully!")
            else:
                print("Contact not found!")

        elif choice == '5':
            if contact_book.contacts:
                print("\nAll Contacts:")
                for contact in contact_book.contacts:
                    print(f"\nName: {contact.name}")
                    print(f"Phone: {contact.phone}")
                    print(f"Email: {contact.email}")
                    print(f"Address: {contact.address}")
            else:
                print("No contacts in the book!")

        elif choice == '6':
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()