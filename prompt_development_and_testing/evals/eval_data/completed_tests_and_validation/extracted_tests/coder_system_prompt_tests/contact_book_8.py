"""
contact_book.py

A simple contact management system that stores contacts in a JSON file.

Functions:
    load_contacts(): Load contacts from JSON file
    save_contacts(): Save contacts to JSON file
    add_contact(): Add a new contact
    search_contact(): Search for a contact
    update_contact(): Update existing contact
    delete_contact(): Delete a contact
    display_menu(): Show user options
    main(): Main program loop

Command Line Usage Example:
    python contact_book.py
"""

import json
import logging
import re
from pathlib import Path
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
CONTACTS_FILE = Path("contacts.json")

def load_contacts() -> List[Dict]:
    """
    Load contacts from JSON file.

    Parameters:
        None

    Returns:
        List[Dict]: List of contact dictionaries
    """
    logger.debug("Loading contacts from file")
    if not CONTACTS_FILE.exists():
        logger.info("Contacts file not found. Creating new contacts list")
        return []
    
    try:
        with CONTACTS_FILE.open('r') as file:
            contacts = json.load(file)
            logger.debug(f"Loaded {len(contacts)} contacts")
            return contacts
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"Error loading contacts: {e}")
        return []

def save_contacts(contacts: List[Dict]) -> None:
    """
    Save contacts to JSON file.

    Parameters:
        contacts (List[Dict]): List of contact dictionaries

    Returns:
        None
    """
    logger.debug(f"Saving {len(contacts)} contacts to file")
    try:
        with CONTACTS_FILE.open('w') as file:
            json.dump(contacts, file, indent=2)
        logger.info("Contacts saved successfully")
    except Exception as e:
        logger.error(f"Error saving contacts: {e}")

def validate_email(email: str) -> bool:
    """
    Validate email format.

    Parameters:
        email (str): Email address to validate

    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.

    Parameters:
        phone (str): Phone number to validate

    Returns:
        bool: True if valid, False otherwise
    """
    return phone.isdigit() and len(phone) >= 10

def add_contact(contacts: List[Dict]) -> None:
    """
    Add a new contact to the list.

    Parameters:
        contacts (List[Dict]): List of existing contacts

    Returns:
        None
    """
    logger.debug("Adding new contact")
    
    name = input("Enter name: ").strip()
    if not name:
        logger.warning("Name cannot be empty")
        return

    phone = input("Enter phone number: ").strip()
    if not validate_phone(phone):
        logger.warning("Invalid phone number")
        return

    email = input("Enter email: ").strip()
    if email and not validate_email(email):
        logger.warning("Invalid email format")
        return

    address = input("Enter address: ").strip()

    contact = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }
    
    contacts.append(contact)
    save_contacts(contacts)
    logger.info("Contact added successfully")

def search_contact(contacts: List[Dict]) -> Optional[Dict]:
    """
    Search for a contact by name.

    Parameters:
        contacts (List[Dict]): List of contacts to search

    Returns:
        Optional[Dict]: Found contact or None
    """
    search_term = input("Enter name to search: ").strip().lower()
    logger.debug(f"Searching for: {search_term}")
    
    for contact in contacts:
        if search_term in contact["name"].lower():
            print("\nContact found:")
            for key, value in contact.items():
                print(f"{key.capitalize()}: {value}")
            return contact
    
    logger.info("Contact not found")
    return None

def update_contact(contacts: List[Dict]) -> None:
    """
    Update an existing contact.

    Parameters:
        contacts (List[Dict]): List of contacts

    Returns:
        None
    """
    contact = search_contact(contacts)
    if not contact:
        return

    logger.debug(f"Updating contact: {contact['name']}")
    
    phone = input("Enter new phone number (or press enter to skip): ").strip()
    if phone:
        if not validate_phone(phone):
            logger.warning("Invalid phone number")
            return
        contact["phone"] = phone

    email = input("Enter new email (or press enter to skip): ").strip()
    if email:
        if not validate_email(email):
            logger.warning("Invalid email format")
            return
        contact["email"] = email

    address = input("Enter new address (or press enter to skip): ").strip()
    if address:
        contact["address"] = address

    save_contacts(contacts)
    logger.info("Contact updated successfully")

def delete_contact(contacts: List[Dict]) -> None:
    """
    Delete a contact.

    Parameters:
        contacts (List[Dict]): List of contacts

    Returns:
        None
    """
    contact = search_contact(contacts)
    if not contact:
        return

    logger.debug(f"Deleting contact: {contact['name']}")
    contacts.remove(contact)
    save_contacts(contacts)
    logger.info("Contact deleted successfully")

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
    print("5. Exit")

def main() -> None:
    """
    Main program loop.

    Parameters:
        None

    Returns:
        None
    """
    logger.info("Starting Contact Book application")
    contacts = load_contacts()

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            search_contact(contacts)
        elif choice == "3":
            update_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            logger.info("Exiting application")
            break
        else:
            logger.warning("Invalid choice")

if __name__ == "__main__":
    main()