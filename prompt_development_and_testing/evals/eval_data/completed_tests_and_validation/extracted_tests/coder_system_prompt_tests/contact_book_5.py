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
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
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
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            address=data['address']
        )

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
        logger.debug("Saving contacts to file")
        try:
            with open(self.filename, 'w') as f:
                json.dump([contact.to_dict() for contact in self.contacts], f, indent=2)
            logger.info("Contacts saved successfully")
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
        
    def search_contact(self, name: str) -> List[Contact]:
        """
        Search for contacts by name.
        
        Parameters:
            name (str): Name to search for
            
        Returns:
            List[Contact]: List of matching contacts
        """
        logger.debug(f"Searching for contact: {name}")
        return [contact for contact in self.contacts 
                if name.lower() in contact.name.lower()]
        
    def update_contact(self, name: str, new_contact: Contact) -> bool:
        """
        Update an existing contact.
        
        Parameters:
            name (str): Name of contact to update
            new_contact (Contact): Updated contact information
            
        Returns:
            bool: True if update successful, False otherwise
        """
        logger.debug(f"Updating contact: {name}")
        for i, contact in enumerate(self.contacts):
            if contact.name.lower() == name.lower():
                self.contacts[i] = new_contact
                self.save_contacts()
                logger.info("Contact updated successfully")
                return True
        logger.warning("Contact not found")
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
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                self.contacts.remove(contact)
                self.save_contacts()
                logger.info("Contact deleted successfully")
                return True
        logger.warning("Contact not found")
        return False
        
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
        for contact in self.contacts:
            print(f"\nName: {contact.name}")
            print(f"Phone: {contact.phone}")
            print(f"Email: {contact.email}")
            print(f"Address: {contact.address}")
            print("-" * 30)

def get_contact_info() -> Contact:
    """
    Get contact information from user input.
    
    Parameters:
        None
        
    Returns:
        Contact: New Contact instance with user-provided information
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
        print("\n=== Contact Book Menu ===")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Display All Contacts")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        try:
            if choice == '1':
                contact = get_contact_info()
                contact_book.add_contact(contact)
                print("Contact added successfully!")
                
            elif choice == '2':
                name = input("Enter name to search: ").strip()
                matches = contact_book.search_contact(name)
                if matches:
                    print("\nMatching contacts:")
                    for contact in matches:
                        print(f"\nName: {contact.name}")
                        print(f"Phone: {contact.phone}")
                        print(f"Email: {contact.email}")
                        print(f"Address: {contact.address}")
                else:
                    print("No matching contacts found.")
                    
            elif choice == '3':
                name = input("Enter name of contact to update: ").strip()
                new_contact = get_contact_info()
                if contact_book.update_contact(name, new_contact):
                    print("Contact updated successfully!")
                else:
                    print("Contact not found.")
                    
            elif choice == '4':
                name = input("Enter name of contact to delete: ").strip()
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
                print("Invalid choice. Please enter a number between 1 and 6.")
                
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print("An error occurred. Please try again.")

if __name__ == "__main__":
    main()