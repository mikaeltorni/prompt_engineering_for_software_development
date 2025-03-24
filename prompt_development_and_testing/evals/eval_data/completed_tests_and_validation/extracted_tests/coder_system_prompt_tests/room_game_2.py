"""
text_adventure.py

A simple text-based adventure game where players can navigate rooms,
collect items, and solve simple challenges.

Classes:
    Item: Represents collectible items in the game
    Room: Represents rooms in the game
    Player: Manages player state and inventory
    Game: Main game controller

Command Line Usage Example:
    python text_adventure.py
"""

import random
import time
import sys
import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

class Item:
    """
    Represents an item in the game.
    
    Parameters:
        name (str): Name of the item
        description (str): Description of the item
        
    Returns:
        None
    """
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        logger.debug(f"Created item: {name}")

class Room:
    """
    Represents a room in the game.
    
    Parameters:
        name (str): Name of the room
        description (str): Description of the room
        
    Returns:
        None
    """
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.connections: Dict[str, 'Room'] = {}
        self.items: List[Item] = []
        self.requires_item: Optional[str] = None
        logger.debug(f"Created room: {name}")

    def add_connection(self, direction: str, room: 'Room') -> None:
        """
        Adds a connection to another room.
        
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
    Represents the player in the game.
    
    Parameters:
        name (str): Name of the player
        
    Returns:
        None
    """
    def __init__(self, name: str):
        self.name = name
        self.inventory: List[Item] = []
        self.current_room: Optional[Room] = None
        logger.debug(f"Created player: {name}")

    def take_item(self, item_name: str) -> bool:
        """
        Attempts to take an item from the current room.
        
        Parameters:
            item_name (str): Name of the item to take
            
        Returns:
            bool: True if item was taken, False otherwise
        """
        logger.debug(f"Attempting to take item: {item_name}")
        for item in self.current_room.items:
            if item.name.lower() == item_name.lower():
                self.inventory.append(item)
                self.current_room.items.remove(item)
                logger.debug(f"Successfully took item: {item_name}")
                return True
        logger.debug(f"Failed to take item: {item_name}")
        return False

class Game:
    """
    Main game controller.
    
    Parameters:
        None
        
    Returns:
        None
    """
    def __init__(self):
        self.rooms: List[Room] = []
        self.player: Optional[Player] = None
        self.setup_game()
        logger.debug("Game initialized")

    def setup_game(self) -> None:
        """
        Sets up the initial game state.
        
        Parameters:
            None
            
        Returns:
            None
        """
        # Create rooms
        entrance = Room("Entrance", "You are at the entrance of a mysterious house.")
        living_room = Room("Living Room", "A cozy living room with old furniture.")
        kitchen = Room("Kitchen", "A kitchen with a strange smell.")
        basement = Room("Basement", "A dark and scary basement.")

        # Create connections
        entrance.add_connection("north", living_room)
        living_room.add_connection("south", entrance)
        living_room.add_connection("east", kitchen)
        kitchen.add_connection("west", living_room)
        kitchen.add_connection("down", basement)
        basement.add_connection("up", kitchen)

        # Add items
        key = Item("key", "A rusty old key")
        flashlight = Item("flashlight", "A working flashlight")
        entrance.items.append(key)
        living_room.items.append(flashlight)

        # Set requirements
        basement.requires_item = "flashlight"

        self.rooms = [entrance, living_room, kitchen, basement]
        logger.debug("Game setup completed")

    def start(self) -> None:
        """
        Starts the game.
        
        Parameters:
            None
            
        Returns:
            None
        """
        print("\nWelcome to the Text Adventure Game!")
        player_name = input("Enter your name: ")
        self.player = Player(player_name)
        self.player.current_room = self.rooms[0]  # Start at entrance
        logger.info(f"Game started with player: {player_name}")
        
        self.game_loop()

    def game_loop(self) -> None:
        """
        Main game loop.
        
        Parameters:
            None
            
        Returns:
            None
        """
        while True:
            print(f"\n=== {self.player.current_room.name} ===")
            print(self.player.current_room.description)
            
            if self.player.current_room.items:
                print("\nItems in room:")
                for item in self.player.current_room.items:
                    print(f"- {item.name}")

            print("\nPossible directions:", ", ".join(self.player.current_room.connections.keys()))
            
            command = input("\nWhat would you like to do? ").lower().split()
            
            if not command:
                continue

            self.process_command(command)

    def process_command(self, command: List[str]) -> None:
        """
        Processes a player command.
        
        Parameters:
            command (List[str]): List of command words
            
        Returns:
            None
        """
        logger.debug(f"Processing command: {command}")
        
        action = command[0]

        if action == "quit":
            print("Thanks for playing!")
            sys.exit()

        elif action == "inventory":
            if self.player.inventory:
                print("\nYour inventory:")
                for item in self.player.inventory:
                    print(f"- {item.name}")
            else:
                print("\nYour inventory is empty.")

        elif action == "take" and len(command) > 1:
            item_name = command[1]
            if self.player.take_item(item_name):
                print(f"Took the {item_name}.")
            else:
                print(f"There is no {item_name} here.")

        elif action in self.player.current_room.connections:
            next_room = self.player.current_room.connections[action]
            
            if next_room.requires_item:
                has_required_item = any(item.name.lower() == next_room.requires_item.lower() 
                                      for item in self.player.inventory)
                if not has_required_item:
                    print(f"You need a {next_room.requires_item} to enter this room!")
                    return

            self.player.current_room = next_room
            print(f"Moving to {next_room.name}...")
            time.sleep(1)

        else:
            print("Invalid command! Available commands: [direction], take [item], inventory, quit")

def main():
    """
    Main function to start the game.
    
    Parameters:
        None
        
    Returns:
        None
    """
    game = Game()
    try:
        game.start()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        sys.exit()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print("\nAn error occurred. The game has to terminate.")
        sys.exit(1)

if __name__ == "__main__":
    main()