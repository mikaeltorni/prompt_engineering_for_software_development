"""
text_adventure.py

A simple text-based adventure game where players can explore rooms,
collect items, and solve challenges.

Functions:
    main(): Main game loop
    setup_game(): Initialize game state
    process_command(command: str, game: Game): Process user input

Command Line Usage Example:
    python text_adventure.py
"""

import logging
import random
import time
import sys
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
    """
    def __init__(self, name: str, description: str):
        """
        Initialize a room.

        Parameters:
            name (str): Name of the room
            description (str): Description of the room

        Returns:
            None
        """
        self.name = name
        self.description = description
        self.items: List[str] = []
        self.connections: Dict[str, 'Room'] = {}
        logger.debug(f"Created room: {name}")

    def add_connection(self, direction: str, room: 'Room') -> None:
        """
        Add a connection to another room.

        Parameters:
            direction (str): Direction of the connection
            room (Room): Room to connect to

        Returns:
            None
        """
        self.connections[direction] = room
        logger.debug(f"Added connection from {self.name} to {room.name} in direction {direction}")

class Player:
    """
    Represents the player character.
    """
    def __init__(self):
        """
        Initialize the player.

        Parameters:
            None

        Returns:
            None
        """
        self.inventory: List[str] = []
        self.current_room: Optional[Room] = None
        self.max_inventory = 5
        logger.debug("Player initialized")

    def take_item(self, item: str) -> bool:
        """
        Add an item to the player's inventory.

        Parameters:
            item (str): Item to add to inventory

        Returns:
            bool: True if successful, False if inventory is full
        """
        if len(self.inventory) >= self.max_inventory:
            logger.warning("Inventory full")
            return False
        self.inventory.append(item)
        logger.debug(f"Added {item} to inventory")
        return True

class Game:
    """
    Main game class that manages game state.
    """
    def __init__(self):
        """
        Initialize the game.

        Parameters:
            None

        Returns:
            None
        """
        self.player = Player()
        self.rooms: Dict[str, Room] = {}
        self.running = True
        logger.debug("Game initialized")

    def setup_rooms(self) -> None:
        """
        Set up the game rooms and their connections.

        Parameters:
            None

        Returns:
            None
        """
        # Create rooms
        self.rooms["hall"] = Room("Hall", "A grand entrance hall with marble floors.")
        self.rooms["kitchen"] = Room("Kitchen", "A warm kitchen with a pleasant aroma.")
        self.rooms["library"] = Room("Library", "A quiet library filled with old books.")
        self.rooms["garden"] = Room("Garden", "A beautiful garden with flowers.")

        # Add connections
        self.rooms["hall"].add_connection("north", self.rooms["library"])
        self.rooms["hall"].add_connection("east", self.rooms["kitchen"])
        self.rooms["hall"].add_connection("south", self.rooms["garden"])
        
        self.rooms["library"].add_connection("south", self.rooms["hall"])
        self.rooms["kitchen"].add_connection("west", self.rooms["hall"])
        self.rooms["garden"].add_connection("north", self.rooms["hall"])

        # Add items to rooms
        self.rooms["kitchen"].items.extend(["key", "apple"])
        self.rooms["library"].items.extend(["book", "candle"])
        self.rooms["garden"].items.extend(["flower", "stone"])

        # Set starting room
        self.player.current_room = self.rooms["hall"]
        logger.debug("Rooms setup complete")

def process_command(command: str, game: Game) -> None:
    """
    Process player commands.

    Parameters:
        command (str): Player's input command
        game (Game): Current game instance

    Returns:
        None
    """
    logger.debug(f"Processing command: {command}")
    
    words = command.lower().split()
    if not words:
        return

    if words[0] == "go":
        if len(words) < 2:
            print("Go where?")
            return
            
        direction = words[1]
        if direction in game.player.current_room.connections:
            game.player.current_room = game.player.current_room.connections[direction]
            print(f"You go {direction} to the {game.player.current_room.name}.")
            print(game.player.current_room.description)
        else:
            print("You can't go that way!")

    elif words[0] == "look":
        print(f"\nYou are in the {game.player.current_room.name}")
        print(game.player.current_room.description)
        if game.player.current_room.items:
            print(f"You see: {', '.join(game.player.current_room.items)}")
        print("\nExits:", ", ".join(game.player.current_room.connections.keys()))

    elif words[0] == "take":
        if len(words) < 2:
            print("Take what?")
            return
            
        item = words[1]
        if item in game.player.current_room.items:
            if game.player.take_item(item):
                game.player.current_room.items.remove(item)
                print(f"You take the {item}.")
            else:
                print("Your inventory is full!")
        else:
            print("You don't see that here.")

    elif words[0] == "inventory":
        if game.player.inventory:
            print("You are carrying:", ", ".join(game.player.inventory))
        else:
            print("Your inventory is empty.")

    elif words[0] == "quit":
        print("Thanks for playing!")
        game.running = False

    elif words[0] == "help":
        print("\nAvailable commands:")
        print("  go <direction> - Move in a direction (north, south, east, west)")
        print("  look - Look around the current room")
        print("  take <item> - Pick up an item")
        print("  inventory - Show your inventory")
        print("  quit - Exit the game")
        print("  help - Show this help message")

    else:
        print("I don't understand that command. Type 'help' for available commands.")

def main() -> None:
    """
    Main game loop.

    Parameters:
        None

    Returns:
        None
    """
    print("\nWelcome to the Text Adventure Game!")
    print("Type 'help' for a list of commands.\n")

    game = Game()
    game.setup_rooms()

    while game.running:
        try:
            command = input("\nWhat would you like to do? ").strip()
            if command:
                process_command(command, game)
            else:
                print("Please enter a command. Type 'help' for available commands.")
        except KeyboardInterrupt:
            print("\nGame terminated by user.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print("An error occurred. Please try again.")

if __name__ == "__main__":
    main()