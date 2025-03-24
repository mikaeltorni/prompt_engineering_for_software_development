"""
text_adventure.py

A simple text-based adventure game where players can navigate rooms,
collect items, and solve simple challenges.

Functions:
    main(): Main game loop
    
Command Line Usage Example:
    python text_adventure.py
"""

import logging
import random
import sys
import time
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

class Room:
    """
    Represents a room in the game world.
    
    Parameters:
        name (str): Name of the room
        description (str): Description of the room
        items (List[str]): Items available in the room
        
    Returns:
        None
    """
    def __init__(self, name: str, description: str, items: List[str]):
        self.name = name
        self.description = description
        self.items = items
        self.connections: Dict[str, 'Room'] = {}
        logger.debug(f"Created room: {name} | items: {items}")

    def connect_room(self, direction: str, room: 'Room') -> None:
        """
        Connects this room to another room in a specific direction.
        
        Parameters:
            direction (str): Direction to connect room
            room (Room): Room to connect to
            
        Returns:
            None
        """
        self.connections[direction] = room
        logger.debug(f"Connected {self.name} to {room.name} in direction {direction}")

class Player:
    """
    Represents the player character in the game.
    
    Parameters:
        None
        
    Returns:
        None
    """
    def __init__(self):
        self.inventory: List[str] = []
        self.current_room: Optional[Room] = None
        logger.debug("Created new player")

    def move(self, direction: str) -> bool:
        """
        Moves the player in the specified direction if possible.
        
        Parameters:
            direction (str): Direction to move
            
        Returns:
            bool: True if movement successful, False otherwise
        """
        logger.debug(f"Attempting to move {direction}")
        if direction in self.current_room.connections:
            self.current_room = self.current_room.connections[direction]
            logger.debug(f"Moved to {self.current_room.name}")
            return True
        return False

    def take_item(self, item: str) -> bool:
        """
        Attempts to take an item from the current room.
        
        Parameters:
            item (str): Item to take
            
        Returns:
            bool: True if item was taken, False otherwise
        """
        logger.debug(f"Attempting to take {item}")
        if item in self.current_room.items:
            self.current_room.items.remove(item)
            self.inventory.append(item)
            logger.debug(f"Took {item}")
            return True
        return False

class Game:
    """
    Main game class that manages game state and logic.
    
    Parameters:
        None
        
    Returns:
        None
    """
    def __init__(self):
        self.player = Player()
        self.setup_game()
        logger.debug("Game initialized")

    def setup_game(self) -> None:
        """
        Sets up the initial game state including rooms and items.
        
        Parameters:
            None
            
        Returns:
            None
        """
        # Create rooms
        entrance = Room("Entrance", "A dimly lit entrance hall.", ["key"])
        living_room = Room("Living Room", "A cozy room with a fireplace.", ["book"])
        kitchen = Room("Kitchen", "A clean kitchen with modern appliances.", ["apple"])
        
        # Connect rooms
        entrance.connect_room("north", living_room)
        living_room.connect_room("south", entrance)
        living_room.connect_room("east", kitchen)
        kitchen.connect_room("west", living_room)
        
        # Set starting room
        self.player.current_room = entrance
        logger.debug("Game setup complete")

    def process_command(self, command: str) -> bool:
        """
        Processes player commands and executes corresponding actions.
        
        Parameters:
            command (str): Player's command
            
        Returns:
            bool: True to continue game, False to exit
        """
        logger.debug(f"Processing command: {command}")
        
        # Split the command into words
        words = command.lower().split()
        
        if not words:
            print("Please enter a command.")
            return True

        if words[0] == "quit":
            return False
        
        elif words[0] == "look":
            self.display_room()
            
        elif words[0] == "inventory":
            if self.player.inventory:
                print("You are carrying:", ", ".join(self.player.inventory))
            else:
                print("Your inventory is empty.")
                
        elif words[0] == "go" and len(words) > 1:
            direction = words[1]
            if not self.player.move(direction):
                print(f"You can't go {direction}.")
            else:
                self.display_room()
                
        elif words[0] == "take" and len(words) > 1:
            item = words[1]
            if self.player.take_item(item):
                print(f"You took the {item}.")
            else:
                print(f"There is no {item} here.")
                
        else:
            print("I don't understand that command.")
            
        return True

    def display_room(self) -> None:
        """
        Displays the current room description and available items.
        
        Parameters:
            None
            
        Returns:
            None
        """
        room = self.player.current_room
        print(f"\n=== {room.name} ===")
        print(room.description)
        
        if room.items:
            print("You see:", ", ".join(room.items))
            
        print("Exits:", ", ".join(room.connections.keys()))

def main() -> None:
    """
    Main game loop.
    
    Parameters:
        None
        
    Returns:
        None
    """
    game = Game()
    print("\nWelcome to the Text Adventure!")
    print("\nCommands: go <direction>, take <item>, look, inventory, quit")
    
    game.display_room()
    
    while True:
        try:
            command = input("\nWhat would you like to do? ").strip()
            if not game.process_command(command):
                print("Thanks for playing!")
                break
                
        except KeyboardInterrupt:
            print("\nGame terminated by user.")
            sys.exit(0)
            
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print("An error occurred. Please try again.")

if __name__ == "__main__":
    main()