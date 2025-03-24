"""
contact_book.py

A simple contact book application that stores contacts in a JSON file.

Classes:
    Contact: Represents a single contact
    ContactBook: Manages the collection of contacts

Functions:
    main(): Main program loop

Command Line Usage Example:
    python contact_book.py
"""

import json
import re
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
        
    def to_dict(self) -> dict:
        """
        Convert contact to dictionary format.
        
        Parameters:
            None
            
        Returns:
            dict: Dictionary representation of the contact
        """
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }
        
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number format.
        
        Parameters:
            phone (str): Phone number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address format.
        
        Parameters:
            email (str): Email address to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

class ContactBook:
    """
    Manages a collection of contacts with save/load functionality.
    """
    
    def __init__(self, filename: str = "contacts.json"):
        """
        Initialize contact book.
        
        Parameters:
            filename (str): Name of the file to store contacts
            
        Returns:
            None
        """
        self.filename = filename
        self.contacts: Dict[str, Contact] = {}
        self.load_contacts()
        
    def add_contact(self, contact: Contact) -> bool:
        """
        Add a new contact to the book.
        
        Parameters:
            contact (Contact): Contact object to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug(f"Adding contact: {contact.name}")
        
        if not contact.validate_phone(contact.phone):
            logger.error("Invalid phone number format")
            return False
            
        if not contact.validate_email(contact.email):
            logger.error("Invalid email format")
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
            bool: True if successful, False otherwise
        """
        logger.debug(f"Updating contact: {name}")
        
        if name not in self.contacts:
            logger.error(f"Contact not found: {name}")
            return False
            
        if not new_contact.validate_phone(new_contact.phone):
            logger.error("Invalid phone number format")
            return False
            
        if not new_contact.validate_email(new_contact.email):
            logger.error("Invalid email format")
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
            bool: True if successful, False otherwise
        """
        logger.debug(f"Deleting contact: {name}")
        
        if name not in self.contacts:
            logger.error(f"Contact not found: {name}")
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
        for name, contact in self.contacts.items():
            print(f"\nName: {contact.name}")
            print(f"Phone: {contact.phone}")
            print(f"Email: {contact.email}")
            print(f"Address: {contact.address}")
            print("-" * 30)
            
    def save_contacts(self) -> None:
        """
        Save contacts to JSON file.
        
        Parameters:
            None
            
        Returns:
            None
        """
        logger.debug(f"Saving contacts to {self.filename}")
        
        contacts_dict = {name: contact.to_dict() for name, contact in self.contacts.items()}
        try:
            with open(self.filename, 'w') as f:
                json.dump(contacts_dict, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving contacts: {e}")
            
    def load_contacts(self) -> None:
        """
        Load contacts from JSON file.
        
        Parameters:
            None
            
        Returns:
            None
        """
        logger.debug(f"Loading contacts from {self.filename}")
        
        try:
            if Path(self.filename).exists():
                with open(self.filename, 'r') as f:
                    contacts_dict = json.load(f)
                    self.contacts = {
                        name: Contact(**data)
                        for name, data in contacts_dict.items()
                    }
        except Exception as e:
            logger.error(f"Error loading contacts: {e}")
            self.contacts = {}

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
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Display All Contacts")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            email = input("Enter email: ")
            address = input("Enter address: ")
            
            contact = Contact(name, phone, email, address)
            if contact_book.add_contact(contact):
                print("Contact added successfully!")
            else:
                print("Failed to add contact. Please check the input format.")
                
        elif choice == '2':
            name = input("Enter name to search: ")
            contact = contact_book.search_contact(name)
            if contact:
                print(f"\nName: {contact.name}")
                print(f"Phone: {contact.phone}")
                print(f"Email: {contact.email}")
                print(f"Address: {contact.address}")
            else:
                print("Contact not found.")
                
        elif choice == '3':
            name = input("Enter name to update: ")
            if contact_book.search_contact(name):
                phone = input("Enter new phone: ")
                email = input("Enter new email: ")
                address = input("Enter new address: ")
                
                new_contact = Contact(name, phone, email, address)
                if contact_book.update_contact(name, new_contact):
                    print("Contact updated successfully!")
                else:
                    print("Failed to update contact. Please check the input format.")
            else:
                print("Contact not found.")
                
        elif choice == '4':
            name = input("Enter name to delete: ")
            if contact_book.delete_contact(name):
                print("Contact deleted successfully!")
            else:
                print("Contact not found.")
                
        elif choice == '5':
            contact_book.display_contacts()
            
        elif choice == '6':
            print("Goodbye!")
            sys.exit(0)
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()