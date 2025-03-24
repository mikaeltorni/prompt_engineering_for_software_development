"""
text_adventure.py

A simple text-based adventure game where players can explore rooms,
collect items, and solve simple challenges.

Functions:
    setup_game(): Initialize game state
    play_game(): Main game loop
    process_command(command: str, player: Player): Process player commands
    display_help(): Show available commands

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
        self.connections: Dict[str, 'Room'] = {}
        self.items: List[str] = []
        logger.debug(f"Created room: {name}")

class Player:
    """
    Represents the player character.
    """
    def __init__(self, current_room: Room):
        """
        Initialize the player.
        
        Parameters:
            current_room (Room): Starting room for the player
            
        Returns:
            None
        """
        self.current_room = current_room
        self.inventory: List[str] = []
        logger.debug("Player initialized")

def setup_game() -> Player:
    """
    Initialize the game world and return the player object.
    
    Parameters:
        None
        
    Returns:
        Player: Initialized player object
    """
    logger.info("Setting up game world")
    
    # Create rooms
    entrance = Room("Entrance Hall", "A grand entrance hall with marble floors.")
    library = Room("Library", "A dusty library filled with ancient books.")
    kitchen = Room("Kitchen", "A medieval kitchen with a cold fireplace.")
    cellar = Room("Cellar", "A dark cellar with mysterious boxes.")
    
    # Connect rooms
    entrance.connections = {"north": library, "east": kitchen}
    library.connections = {"south": entrance, "east": cellar}
    kitchen.connections = {"west": entrance, "north": cellar}
    cellar.connections = {"west": library, "south": kitchen}
    
    # Add items to rooms
    entrance.items = ["key"]
    library.items = ["book"]
    kitchen.items = ["knife"]
    cellar.items = ["potion"]
    
    return Player(entrance)

def display_help() -> None:
    """
    Display available commands to the player.
    
    Parameters:
        None
        
    Returns:
        None
    """
    print("\nAvailable commands:")
    print("- look: Look around the current room")
    print("- go <direction>: Move in a direction (north, south, east, west)")
    print("- take <item>: Pick up an item")
    print("- inventory: Show your inventory")
    print("- help: Show this help message")
    print("- quit: Exit the game")

def process_command(command: str, player: Player) -> bool:
    """
    Process player commands.
    
    Parameters:
        command (str): Player's input command
        player (Player): Player object
        
    Returns:
        bool: True if game should continue, False if game should end
    """
    logger.debug(f"Processing command: {command}")
    
    command = command.lower().strip()
    words = command.split()
    
    if not words:
        print("Please enter a command. Type 'help' for available commands.")
        return True
        
    action = words[0]
    
    try:
        if action == "quit":
            print("Thanks for playing!")
            return False
            
        elif action == "help":
            display_help()
            
        elif action == "look":
            print(f"\n=== {player.current_room.name} ===")
            print(player.current_room.description)
            if player.current_room.items:
                print("Items here:", ", ".join(player.current_room.items))
            print("Exits:", ", ".join(player.current_room.connections.keys()))
            
        elif action == "inventory":
            if player.inventory:
                print("You are carrying:", ", ".join(player.inventory))
            else:
                print("Your inventory is empty.")
                
        elif action == "take":
            if len(words) < 2:
                print("Take what? Please specify an item.")
                return True
                
            item = words[1]
            if item in player.current_room.items:
                player.current_room.items.remove(item)
                player.inventory.append(item)
                print(f"Taken: {item}")
                logger.info(f"Player took {item}")
            else:
                print("That item isn't here.")
                
        elif action == "go":
            if len(words) < 2:
                print("Go where? Please specify a direction.")
                return True
                
            direction = words[1]
            if direction in player.current_room.connections:
                player.current_room = player.current_room.connections[direction]
                print(f"\nYou go {direction}.")
                logger.info(f"Player moved {direction} to {player.current_room.name}")
                # Automatically look around in the new room
                print(f"\n=== {player.current_room.name} ===")
                print(player.current_room.description)
                if player.current_room.items:
                    print("Items here:", ", ".join(player.current_room.items))
                print("Exits:", ", ".join(player.current_room.connections.keys()))
            else:
                print("You can't go that way.")
        else:
            print("Unknown command. Type 'help' for available commands.")
            
    except Exception as e:
        logger.error(f"Error processing command: {e}")
        print("Something went wrong. Please try again.")
        
    return True

def play_game() -> None:
    """
    Main game loop.
    
    Parameters:
        None
        
    Returns:
        None
    """
    print("\nWelcome to the Text Adventure!")
    print("Type 'help' for a list of commands.")
    
    player = setup_game()
    logger.info("Game started")
    
    # Initial room description
    print(f"\n=== {player.current_room.name} ===")
    print(player.current_room.description)
    if player.current_room.items:
        print("Items here:", ", ".join(player.current_room.items))
    print("Exits:", ", ".join(player.current_room.connections.keys()))
    
    # Main game loop
    while True:
        try:
            command = input("\nWhat would you like to do? ").strip()
            if not process_command(command, player):
                break
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    try:
        play_game()
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        print("A critical error occurred. The game must exit.")
        sys.exit(1)