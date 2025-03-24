"""
contact_book.py

A simple contact book application that stores contacts in a JSON file.

Classes:
    Contact: Represents a single contact
    ContactBook: Manages the collection of contacts

Functions:
    display_menu(): Displays the main menu
    get_contact_info(): Gets contact information from user
    main(): Main program loop

Command Line Usage Example:
    python contact_book.py
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional
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
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }

class ContactBook:
    """
    Manages a collection of contacts with operations for adding, searching,
    updating, and deleting contacts.
    """
    def __init__(self, filename: str = 'contacts.json'):
        """
        Initialize the contact book.

        Parameters:
            filename (str): Name of the JSON file to store contacts

        Returns:
            None
        """
        self.filename = filename
        self.contacts: Dict[str, Contact] = {}
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
                    contacts_dict = json.load(f)
                    for name, data in contacts_dict.items():
                        self.contacts[name] = Contact(
                            data['name'],
                            data['phone'],
                            data['email'],
                            data['address']
                        )
                logger.info(f"Loaded {len(self.contacts)} contacts")
            except json.JSONDecodeError as e:
                logger.error(f"Error loading contacts: {e}")
                print("Error loading contacts file. Starting with empty contact book.")

    def save_contacts(self) -> None:
        """
        Save contacts to JSON file.

        Parameters:
            None

        Returns:
            None
        """
        logger.debug("Saving contacts to file")
        contacts_dict = {name: contact.to_dict() 
                        for name, contact in self.contacts.items()}
        try:
            with open(self.filename, 'w') as f:
                json.dump(contacts_dict, f, indent=4)
            logger.info("Contacts saved successfully")
        except Exception as e:
            logger.error(f"Error saving contacts: {e}")
            print("Error saving contacts to file.")

    def add_contact(self, contact: Contact) -> bool:
        """
        Add a new contact to the book.

        Parameters:
            contact (Contact): Contact object to add

        Returns:
            bool: True if successful, False if contact already exists
        """
        logger.debug(f"Adding contact: {contact.name}")
        if contact.name in self.contacts:
            logger.warning(f"Contact {contact.name} already exists")
            return False
        self.contacts[contact.name] = contact
        self.save_contacts()
        return True

    def search_contact(self, name: str) -> Optional[Contact]:
        """
        Search for a contact by name.

        Parameters:
            name (str): Name to search for

        Returns:
            Optional[Contact]: Contact if found, None otherwise
        """
        logger.debug(f"Searching for contact: {name}")
        return self.contacts.get(name)

    def update_contact(self, name: str, new_contact: Contact) -> bool:
        """
        Update an existing contact.

        Parameters:
            name (str): Name of contact to update
            new_contact (Contact): New contact information

        Returns:
            bool: True if successful, False if contact doesn't exist
        """
        logger.debug(f"Updating contact: {name}")
        if name not in self.contacts:
            logger.warning(f"Contact {name} not found")
            return False
        self.contacts[name] = new_contact
        self.save_contacts()
        return True

    def delete_contact(self, name: str) -> bool:
        """
        Delete a contact by name.

        Parameters:
            name (str): Name of contact to delete

        Returns:
            bool: True if successful, False if contact doesn't exist
        """
        logger.debug(f"Deleting contact: {name}")
        if name not in self.contacts:
            logger.warning(f"Contact {name} not found")
            return False
        del self.contacts[name]
        self.save_contacts()
        return True

    def display_contacts(self) -> None:
        """
        Display all contacts.

        Parameters:
            None

        Returns:
            None
        """
        logger.debug("Displaying all contacts")
        if not self.contacts:
            print("\nNo contacts found.")
            return
        
        print("\nContacts:")
        print("-" * 40)
        for contact in self.contacts.values():
            print(f"Name: {contact.name}")
            print(f"Phone: {contact.phone}")
            print(f"Email: {contact.email}")
            print(f"Address: {contact.address}")
            print("-" * 40)

def display_menu() -> None:
    """
    Display the main menu.

    Parameters:
        None

    Returns:
        None
    """
    print("\nContact Book Menu:")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Display All Contacts")
    print("6. Exit")

def get_contact_info() -> Contact:
    """
    Get contact information from user input.

    Parameters:
        None

    Returns:
        Contact: New contact object with user-provided information
    """
    print("\nEnter contact information:")
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    address = input("Address: ").strip()
    return Contact(name, phone, email, address)

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
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            contact = get_contact_info()
            if contact_book.add_contact(contact):
                print("Contact added successfully!")
            else:
                print("Contact already exists!")

        elif choice == '2':
            name = input("Enter name to search: ").strip()
            contact = contact_book.search_contact(name)
            if contact:
                print("\nContact found:")
                print(f"Name: {contact.name}")
                print(f"Phone: {contact.phone}")
                print(f"Email: {contact.email}")
                print(f"Address: {contact.address}")
            else:
                print("Contact not found!")

        elif choice == '3':
            name = input("Enter name of contact to update: ").strip()
            if contact_book.search_contact(name):
                new_contact = get_contact_info()
                if contact_book.update_contact(name, new_contact):
                    print("Contact updated successfully!")
            else:
                print("Contact not found!")

        elif choice == '4':
            name = input("Enter name of contact to delete: ").strip()
            if contact_book.delete_contact(name):
                print("Contact deleted successfully!")
            else:
                print("Contact not found!")

        elif choice == '5':
            contact_book.display_contacts()

        elif choice == '6':
            print("Thank you for using Contact Book!")
            sys.exit(0)

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()