"""
text_adventure.py

A simple text-based adventure game where players can navigate rooms,
collect items, and solve simple challenges.

Classes:
    Room: Represents a room in the game
    Player: Represents the player and their inventory
    Game: Controls the game flow and state

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
        
    Returns:
        None
    """
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.connections: Dict[str, 'Room'] = {}
        self.items: List[str] = []
        self.challenge: Optional[str] = None
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
    Represents the player character.
    
    Parameters:
        None
        
    Returns:
        None
    """
    def __init__(self):
        self.current_room: Optional[Room] = None
        self.inventory: List[str] = []
        logger.debug("Created player")

    def move(self, direction: str) -> bool:
        """
        Moves the player in the specified direction.
        
        Parameters:
            direction (str): Direction to move
            
        Returns:
            bool: True if movement successful, False otherwise
        """
        if direction in self.current_room.connections:
            self.current_room = self.current_room.connections[direction]
            logger.info(f"Player moved to {self.current_room.name}")
            return True
        logger.warning(f"Invalid direction: {direction}")
        return False

    def take_item(self, item: str) -> bool:
        """
        Picks up an item from the current room.
        
        Parameters:
            item (str): Item to pick up
            
        Returns:
            bool: True if item was picked up, False otherwise
        """
        if item in self.current_room.items:
            self.current_room.items.remove(item)
            self.inventory.append(item)
            logger.info(f"Player picked up {item}")
            return True
        logger.warning(f"Item not found: {item}")
        return False

    def drop_item(self, item: str) -> bool:
        """
        Drops an item in the current room.
        
        Parameters:
            item (str): Item to drop
            
        Returns:
            bool: True if item was dropped, False otherwise
        """
        if item in self.inventory:
            self.inventory.remove(item)
            self.current_room.items.append(item)
            logger.info(f"Player dropped {item}")
            return True
        logger.warning(f"Item not in inventory: {item}")
        return False

class Game:
    """
    Controls the game flow and state.
    
    Parameters:
        None
        
    Returns:
        None
    """
    def __init__(self):
        self.player = Player()
        self.rooms: List[Room] = []
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
        entrance = Room("Entrance", "You are at the entrance of a mysterious castle.")
        hall = Room("Great Hall", "A grand hall with ancient tapestries.")
        library = Room("Library", "Dusty books line the walls.")
        kitchen = Room("Kitchen", "A medieval kitchen with a cold fireplace.")
        
        # Add connections
        entrance.add_connection("north", hall)
        hall.add_connection("south", entrance)
        hall.add_connection("east", library)
        hall.add_connection("west", kitchen)
        library.add_connection("west", hall)
        kitchen.add_connection("east", hall)
        
        # Add items
        entrance.items = ["key"]
        library.items = ["book"]
        kitchen.items = ["knife"]
        
        # Add challenges
        library.challenge = "answer_riddle"
        
        self.rooms = [entrance, hall, library, kitchen]
        self.player.current_room = entrance
        logger.info("Game setup completed")

    def handle_command(self, command: str) -> bool:
        """
        Processes player commands.
        
        Parameters:
            command (str): Player's command
            
        Returns:
            bool: True to continue game, False to quit
        """
        logger.debug(f"Processing command: {command}")
        words = command.lower().split()
        
        if not words:
            print("Please enter a command.")
            return True

        if words[0] == "quit":
            return False
        
        if words[0] == "look":
            self.look_around()
            return True
            
        if words[0] == "inventory":
            self.show_inventory()
            return True
            
        if len(words) < 2:
            print("Invalid command format.")
            return True
            
        if words[0] == "go":
            return self.handle_movement(words[1])
            
        if words[0] == "take":
            return self.handle_take(words[1])
            
        if words[0] == "drop":
            return self.handle_drop(words[1])
            
        print("Unknown command.")
        return True

    def look_around(self) -> None:
        """
        Displays current room information.
        
        Parameters:
            None
            
        Returns:
            None
        """
        room = self.player.current_room
        print(f"\n=== {room.name} ===")
        print(room.description)
        
        if room.items:
            print(f"Items here: {', '.join(room.items)}")
            
        if room.connections:
            print(f"Exits: {', '.join(room.connections.keys())}")

    def show_inventory(self) -> None:
        """
        Displays player's inventory.
        
        Parameters:
            None
            
        Returns:
            None
        """
        if self.player.inventory:
            print(f"You are carrying: {', '.join(self.player.inventory)}")
        else:
            print("Your inventory is empty.")

    def handle_movement(self, direction: str) -> bool:
        """
        Handles player movement commands.
        
        Parameters:
            direction (str): Direction to move
            
        Returns:
            bool: True to continue game
        """
        if self.player.move(direction):
            self.look_around()
            if self.player.current_room.challenge:
                self.handle_challenge()
        else:
            print(f"You can't go {direction}.")
        return True

    def handle_take(self, item: str) -> bool:
        """
        Handles item pickup commands.
        
        Parameters:
            item (str): Item to take
            
        Returns:
            bool: True to continue game
        """
        if self.player.take_item(item):
            print(f"Taken: {item}")
        else:
            print(f"Can't take {item}.")
        return True

    def handle_drop(self, item: str) -> bool:
        """
        Handles item drop commands.
        
        Parameters:
            item (str): Item to drop
            
        Returns:
            bool: True to continue game
        """
        if self.player.drop_item(item):
            print(f"Dropped: {item}")
        else:
            print(f"Can't drop {item}.")
        return True

    def handle_challenge(self) -> None:
        """
        Handles room challenges.
        
        Parameters:
            None
            
        Returns:
            None
        """
        if self.player.current_room.challenge == "answer_riddle":
            print("\nTo enter this room, you must answer a riddle:")
            print("What has keys, but no locks; space, but no room; and you can enter, but not go in?")
            answer = input("> ").lower().strip()
            if answer == "keyboard":
                print("Correct! You may enter.")
                self.player.current_room.challenge = None
            else:
                print("Incorrect! You are teleported back to the previous room.")
                self.player.move("west")

    def play(self) -> None:
        """
        Main game loop.
        
        Parameters:
            None
            
        Returns:
            None
        """
        print("Welcome to the Text Adventure!")
        print('Enter commands like "go north", "take key", "drop book", "inventory", "look", or "quit"')
        self.look_around()
        
        while True:
            try:
                command = input("\nWhat would you like to do? ").strip()
                if not self.handle_command(command):
                    print("Thanks for playing!")
                    break
            except Exception as e:
                logger.error(f"Error processing command: {e}")
                print("An error occurred. Please try again.")

def main():
    """
    Main entry point for the game.
    
    Parameters:
        None
        
    Returns:
        None
    """
    try:
        game = Game()
        game.play()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print("A fatal error occurred. The game must exit.")
        sys.exit(1)

if __name__ == "__main__":
    main()