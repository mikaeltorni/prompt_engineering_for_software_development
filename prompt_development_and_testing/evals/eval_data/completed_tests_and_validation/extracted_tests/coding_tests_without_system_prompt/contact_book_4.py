import json
import os
from typing import Dict, List

class ContactBook:
    def __init__(self, filename: str = "contacts.json"):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self) -> List[Dict]:
        """Load contacts from JSON file or create empty list if file doesn't exist"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    def save_contacts(self):
        """Save contacts to JSON file"""
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file, indent=2)

    def add_contact(self, name: str, phone: str, email: str):
        """Add a new contact"""
        contact = {
            "name": name,
            "phone": phone,
            "email": email
        }
        self.contacts.append(contact)
        self.save_contacts()
        print(f"Contact {name} added successfully!")

    def search_contact(self, search_term: str) -> List[Dict]:
        """Search for contacts by name or phone number"""
        results = []
        search_term = search_term.lower()
        for contact in self.contacts:
            if (search_term in contact["name"].lower() or 
                search_term in contact["phone"]):
                results.append(contact)
        return results

    def update_contact(self, index: int, name: str, phone: str, email: str):
        """Update an existing contact"""
        if 0 <= index < len(self.contacts):
            self.contacts[index] = {
                "name": name,
                "phone": phone,
                "email": email
            }
            self.save_contacts()
            print(f"Contact updated successfully!")
        else:
            print("Invalid contact index!")

    def delete_contact(self, index: int):
        """Delete a contact"""
        if 0 <= index < len(self.contacts):
            deleted_contact = self.contacts.pop(index)
            self.save_contacts()
            print(f"Contact {deleted_contact['name']} deleted successfully!")
        else:
            print("Invalid contact index!")

    def display_contacts(self):
        """Display all contacts"""
        if not self.contacts:
            print("No contacts found!")
            return
        
        print("\nAll Contacts:")
        print("-" * 50)
        for i, contact in enumerate(self.contacts):
            print(f"{i}. Name: {contact['name']}")
            print(f"   Phone: {contact['phone']}")
            print(f"   Email: {contact['email']}")
            print("-" * 50)

def main():
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
        
        if choice == "1":
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            email = input("Enter email: ")
            contact_book.add_contact(name, phone, email)

        elif choice == "2":
            search_term = input("Enter name or phone number to search: ")
            results = contact_book.search_contact(search_term)
            if results:
                print("\nSearch Results:")
                print("-" * 50)
                for contact in results:
                    print(f"Name: {contact['name']}")
                    print(f"Phone: {contact['phone']}")
                    print(f"Email: {contact['email']}")
                    print("-" * 50)
            else:
                print("No contacts found!")

        elif choice == "3":
            contact_book.display_contacts()
            if contact_book.contacts:
                index = int(input("Enter the index of contact to update: "))
                name = input("Enter new name: ")
                phone = input("Enter new phone number: ")
                email = input("Enter new email: ")
                contact_book.update_contact(index, name, phone, email)

        elif choice == "4":
            contact_book.display_contacts()
            if contact_book.contacts:
                index = int(input("Enter the index of contact to delete: "))
                contact_book.delete_contact(index)

        elif choice == "5":
            contact_book.display_contacts()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()