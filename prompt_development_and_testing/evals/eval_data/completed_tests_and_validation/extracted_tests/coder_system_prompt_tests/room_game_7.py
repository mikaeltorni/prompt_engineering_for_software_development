"""
text_adventure.py

A simple text-based adventure game where players can navigate rooms,
collect items, and interact with their environment.

Classes:
    Player: Manages player inventory and location
    Room: Represents a game room with items and connections
    Game: Main game controller

Command Line Usage Example:
    python text_adventure.py
"""

import logging
import random
import sys
import time
from typing import Dict, List, Optional, Set

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

class Player:
    """
    Represents the player character with inventory management.
    """
    def __init__(self):
        """
        Initialize player with empty inventory.
        
        Parameters:
            None
            
        Returns:
            None
        """
        self.inventory: Set[str] = set()
        self.current_room: Optional[str] = "start"
        logger.debug("Player initialized")

    def add_item(self, item: str) -> None:
        """
        Add an item to player's inventory.
        
        Parameters:
            item (str): Item to add to inventory
            
        Returns:
            None
        """
        logger.debug(f"Adding item: {item}")
        self.inventory.add(item)

    def remove_item(self, item: str) -> bool:
        """
        Remove an item from player's inventory.
        
        Parameters:
            item (str): Item to remove from inventory
            
        Returns:
            bool: True if item was removed, False if not found
        """
        logger.debug(f"Removing item: {item}")
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

class Room:
    """
    Represents a room in the game world.
    """
    def __init__(self, description: str):
        """
        Initialize room with description and empty items.
        
        Parameters:
            description (str): Room description
            
        Returns:
            None
        """
        self.description = description
        self.items: Set[str] = set()
        self.connections: Dict[str, str] = {}
        logger.debug(f"Room initialized with description: {description}")

    def add_connection(self, direction: str, room: str) -> None:
        """
        Add a connection to another room.
        
        Parameters:
            direction (str): Direction of connection
            room (str): Room identifier
            
        Returns:
            None
        """
        logger.debug(f"Adding connection: {direction} -> {room}")
        self.connections[direction] = room

class Game:
    """
    Main game controller class.
    """
    def __init__(self):
        """
        Initialize game with rooms and player.
        
        Parameters:
            None
            
        Returns:
            None
        """
        self.rooms: Dict[str, Room] = {}
        self.player = Player()
        self.setup_game()
        logger.debug("Game initialized")

    def setup_game(self) -> None:
        """
        Set up the initial game state with rooms and items.
        
        Parameters:
            None
            
        Returns:
            None
        """
        # Create rooms
        self.rooms["start"] = Room("You are in the entrance hall. Dusty paintings hang on the walls.")
        self.rooms["kitchen"] = Room("You are in a kitchen. The air smells of old spices.")
        self.rooms["library"] = Room("You are in a library. Books line the shelves.")
        self.rooms["garden"] = Room("You are in an overgrown garden. Flowers bloom despite the neglect.")

        # Add connections
        self.rooms["start"].add_connection("north", "library")
        self.rooms["start"].add_connection("east", "kitchen")
        self.rooms["library"].add_connection("south", "start")
        self.rooms["library"].add_connection("east", "garden")
        self.rooms["kitchen"].add_connection("west", "start")
        self.rooms["kitchen"].add_connection("north", "garden")
        self.rooms["garden"].add_connection("west", "library")
        self.rooms["garden"].add_connection("south", "kitchen")

        # Add items
        self.rooms["kitchen"].items.add("key")
        self.rooms["library"].items.add("book")
        self.rooms["garden"].items.add("flower")
        
        logger.debug("Game setup completed")

    def get_current_room(self) -> Room:
        """
        Get the current room object.
        
        Parameters:
            None
            
        Returns:
            Room: Current room object
        """
        return self.rooms[self.player.current_room]

    def handle_command(self, command: str) -> bool:
        """
        Process player commands.
        
        Parameters:
            command (str): Player's input command
            
        Returns:
            bool: True if game should continue, False if game should end
        """
        logger.debug(f"Processing command: {command}")
        parts = command.lower().split()

        if not parts:
            print("Please enter a command.")
            return True

        if parts[0] == "quit":
            return False

        elif parts[0] == "help":
            self.show_help()

        elif parts[0] == "look":
            self.look_around()

        elif parts[0] == "inventory":
            self.show_inventory()

        elif parts[0] == "go" and len(parts) > 1:
            self.move_player(parts[1])

        elif parts[0] == "take" and len(parts) > 1:
            self.take_item(parts[1])

        elif parts[0] == "drop" and len(parts) > 1:
            self.drop_item(parts[1])

        else:
            print("I don't understand that command. Type 'help' for commands.")

        return True

    def show_help(self) -> None:
        """
        Display available commands.
        
        Parameters:
            None
            
        Returns:
            None
        """
        print("\nAvailable commands:")
        print("  look - Look around the current room")
        print("  inventory - Show your inventory")
        print("  go <direction> - Move in a direction (north/south/east/west)")
        print("  take <item> - Pick up an item")
        print("  drop <item> - Drop an item")
        print("  help - Show this help message")
        print("  quit - Exit the game")

    def look_around(self) -> None:
        """
        Display current room description and contents.
        
        Parameters:
            None
            
        Returns:
            None
        """
        current_room = self.get_current_room()
        print(f"\n{current_room.description}")
        
        if current_room.items:
            print(f"You see: {', '.join(current_room.items)}")
        
        print(f"Exits: {', '.join(current_room.connections.keys())}")

    def show_inventory(self) -> None:
        """
        Display player's inventory.
        
        Parameters:
            None
            
        Returns:
            None
        """
        if self.player.inventory:
            print(f"\nYou are carrying: {', '.join(self.player.inventory)}")
        else:
            print("\nYour inventory is empty.")

    def move_player(self, direction: str) -> None:
        """
        Move player in specified direction if possible.
        
        Parameters:
            direction (str): Direction to move
            
        Returns:
            None
        """
        current_room = self.get_current_room()
        if direction in current_room.connections:
            self.player.current_room = current_room.connections[direction]
            self.look_around()
        else:
            print(f"You can't go {direction}.")

    def take_item(self, item: str) -> None:
        """
        Pick up an item from current room.
        
        Parameters:
            item (str): Item to pick up
            
        Returns:
            None
        """
        current_room = self.get_current_room()
        if item in current_room.items:
            current_room.items.remove(item)
            self.player.add_item(item)
            print(f"Taken: {item}")
        else:
            print(f"There is no {item} here.")

    def drop_item(self, item: str) -> None:
        """
        Drop an item in current room.
        
        Parameters:
            item (str): Item to drop
            
        Returns:
            None
        """
        if self.player.remove_item(item):
            self.get_current_room().items.add(item)
            print(f"Dropped: {item}")
        else:
            print(f"You don't have {item}.")

    def play(self) -> None:
        """
        Main game loop.
        
        Parameters:
            None
            
        Returns:
            None
        """
        print("\nWelcome to the Text Adventure Game!")
        print("Type 'help' for commands.")
        self.look_around()

        while True:
            try:
                command = input("\nWhat would you like to do? ").strip()
                if not self.handle_command(command):
                    print("\nThanks for playing!")
                    break
            except Exception as e:
                logger.error(f"Error processing command: {e}")
                print("An error occurred. Please try again.")

def main():
    """
    Main function to start the game.
    
    Parameters:
        None
        
    Returns:
        None
    """
    game = Game()
    game.play()

if __name__ == "__main__":
    main()