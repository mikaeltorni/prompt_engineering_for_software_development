"""
contact_book.py

A simple contact book application that manages contacts with CRUD operations
and stores them in a JSON file.

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
            Dict: Contact information as dictionary
        """
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }
        
    @staticmethod
    def from_dict(data: Dict) -> 'Contact':
        """
        Create a Contact object from dictionary data.
        
        Parameters:
            data (Dict): Dictionary containing contact information
            
        Returns:
            Contact: New Contact object
        """
        return Contact(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            address=data['address']
        )

class ContactBook:
    """
    Manages a collection of contacts with CRUD operations.
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
                    data = json.load(f)
                    self.contacts = [Contact.from_dict(contact) for contact in data]
                logger.info(f"Loaded {len(self.contacts)} contacts")
            except Exception as e:
                logger.error(f"Error loading contacts: {e}")
                
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
            contact (Contact): Contact to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug(f"Adding contact: {contact.name}")
        if not self._validate_contact(contact):
            return False
        self.contacts.append(contact)
        self.save_contacts()
        return True
        
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
        
    def update_contact(self, old_name: str, new_contact: Contact) -> bool:
        """
        Update an existing contact.
        
        Parameters:
            old_name (str): Name of contact to update
            new_contact (Contact): Updated contact information
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.debug(f"Updating contact: {old_name}")
        for i, contact in enumerate(self.contacts):
            if contact.name.lower() == old_name.lower():
                if self._validate_contact(new_contact):
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
            bool: True if successful, False otherwise
        """
        logger.debug(f"Deleting contact: {name}")
        initial_length = len(self.contacts)
        self.contacts = [c for c in self.contacts if c.name.lower() != name.lower()]
        if len(self.contacts) < initial_length:
            self.save_contacts()
            return True
        return False
        
    def _validate_contact(self, contact: Contact) -> bool:
        """
        Validate contact information.
        
        Parameters:
            contact (Contact): Contact to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        logger.debug(f"Validating contact: {contact.name}")
        
        # Validate email
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, contact.email):
            logger.warning("Invalid email format")
            return False
            
        # Validate phone (simple validation for demonstration)
        phone_pattern = r'^\+?1?\d{9,15}$'
        if not re.match(phone_pattern, contact.phone):
            logger.warning("Invalid phone format")
            return False
            
        return True

def get_user_input(prompt: str, required: bool = True) -> str:
    """
    Get input from user with validation.
    
    Parameters:
        prompt (str): Prompt to display
        required (bool): Whether the input is required
        
    Returns:
        str: User input
    """
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required.")

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
            name = get_user_input("Enter name: ")
            phone = get_user_input("Enter phone: ")
            email = get_user_input("Enter email: ")
            address = get_user_input("Enter address: ", required=False)
            
            contact = Contact(name, phone, email, address)
            if contact_book.add_contact(contact):
                print("Contact added successfully!")
            else:
                print("Failed to add contact. Please check the information.")
                
        elif choice == '2':
            term = get_user_input("Enter search term: ")
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
                
        elif choice == '3':
            old_name = get_user_input("Enter name of contact to update: ")
            name = get_user_input("Enter new name: ")
            phone = get_user_input("Enter new phone: ")
            email = get_user_input("Enter new email: ")
            address = get_user_input("Enter new address: ", required=False)
            
            new_contact = Contact(name, phone, email, address)
            if contact_book.update_contact(old_name, new_contact):
                print("Contact updated successfully!")
            else:
                print("Failed to update contact.")
                
        elif choice == '4':
            name = get_user_input("Enter name of contact to delete: ")
            if contact_book.delete_contact(name):
                print("Contact deleted successfully!")
            else:
                print("Contact not found.")
                
        elif choice == '5':
            if contact_book.contacts:
                print("\nAll Contacts:")
                for contact in contact_book.contacts:
                    print(f"\nName: {contact.name}")
                    print(f"Phone: {contact.phone}")
                    print(f"Email: {contact.email}")
                    print(f"Address: {contact.address}")
            else:
                print("No contacts in the book.")
                
        elif choice == '6':
            print("Goodbye!")
            sys.exit(0)
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()