"""
text_adventure.py

A simple text-based adventure game where players can explore rooms,
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
        Sets up the initial game state with rooms and items.
        
        Parameters:
            None
            
        Returns:
            None
        """
        # Create rooms
        entrance = Room("Entrance Hall", 
                       "A dimly lit hall with ancient tapestries.",
                       ["key"])
        
        library = Room("Library",
                      "Dusty shelves filled with old books.",
                      ["book", "candle"])
        
        kitchen = Room("Kitchen",
                      "A medieval kitchen with a cold fireplace.",
                      ["pot", "apple"])

        # Connect rooms
        entrance.connect_room("north", library)
        entrance.connect_room("east", kitchen)
        library.connect_room("south", entrance)
        kitchen.connect_room("west", entrance)

        self.player.current_room = entrance
        logger.debug("Game setup completed")

    def process_command(self, command: str) -> str:
        """
        Processes player commands and returns feedback.
        
        Parameters:
            command (str): Player's command
            
        Returns:
            str: Feedback message
        """
        logger.debug(f"Processing command: {command}")
        words = command.lower().split()

        if not words:
            return "Please enter a command."

        if words[0] == "go":
            if len(words) < 2:
                return "Go where?"
            direction = words[1]
            if self.player.move(direction):
                return f"You move {direction} to the {self.player.current_room.name}.\n{self.player.current_room.description}"
            return f"You can't go {direction}."

        elif words[0] == "take":
            if len(words) < 2:
                return "Take what?"
            item = words[1]
            if self.player.take_item(item):
                return f"You take the {item}."
            return f"There is no {item} here."

        elif words[0] == "inventory":
            if not self.player.inventory:
                return "Your inventory is empty."
            return f"Inventory: {', '.join(self.player.inventory)}"

        elif words[0] == "look":
            items = ", ".join(self.player.current_room.items) if self.player.current_room.items else "nothing"
            return f"{self.player.current_room.description}\nYou see: {items}"

        elif words[0] == "quit":
            logger.info("Player quit the game")
            print("Thanks for playing!")
            sys.exit(0)

        return "I don't understand that command."

def main() -> None:
    """
    Main game loop.
    
    Parameters:
        None
        
    Returns:
        None
    """
    game = Game()
    print("Welcome to the Text Adventure!")
    print("Commands: go [direction], take [item], inventory, look, quit")
    print("\nYou are in the Entrance Hall.")
    print(game.player.current_room.description)

    while True:
        try:
            command = input("\nWhat would you like to do? ").strip()
            if command:
                response = game.process_command(command)
                print("\n" + response)
            else:
                print("\nPlease enter a command.")
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print("An error occurred. Please try again.")

if __name__ == "__main__":
    main()