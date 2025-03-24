"""
text_adventure.py

A simple text-based adventure game where players can navigate rooms,
collect items, and solve simple challenges.

Functions:
    initialize_game(): Sets up the initial game state
    process_command(command: str): Processes player commands
    display_room(room: dict): Displays current room information
    handle_movement(direction: str): Handles player movement
    handle_inventory(): Displays player inventory
    handle_take(item: str): Handles picking up items
    game_loop(): Main game loop

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

# Global game state
current_room = "entrance"
inventory: List[str] = []
game_running = True

# Game world definition
GAME_WORLD: Dict[str, Dict] = {
    "entrance": {
        "description": "You are at the entrance of a mysterious castle.",
        "exits": {"north": "hall", "east": "garden"},
        "items": ["key"]
    },
    "hall": {
        "description": "You are in a grand hall with ancient tapestries.",
        "exits": {"south": "entrance", "east": "library"},
        "items": ["sword"]
    },
    "garden": {
        "description": "You find yourself in a beautiful garden with strange plants.",
        "exits": {"west": "entrance"},
        "items": ["flower"]
    },
    "library": {
        "description": "Dusty books line the walls of this ancient library.",
        "exits": {"west": "hall"},
        "items": ["book"]
    }
}

def initialize_game() -> None:
    """
    Initialize the game state.

    Parameters:
        None

    Returns:
        None
    """
    logger.info("Initializing new game")
    global current_room, inventory
    current_room = "entrance"
    inventory = []
    display_room(GAME_WORLD[current_room])

def display_room(room: Dict) -> None:
    """
    Display the current room's description and available options.

    Parameters:
        room (Dict): Dictionary containing room information

    Returns:
        None
    """
    logger.debug(f"Displaying room: {current_room}")
    print("\n" + "="*50)
    print(room["description"])
    
    # Show available exits
    exits = room["exits"]
    print("\nAvailable exits:", ", ".join(exits.keys()))
    
    # Show items in the room
    items = room["items"]
    if items:
        print("You see:", ", ".join(items))
    print("="*50)

def handle_movement(direction: str) -> None:
    """
    Handle player movement between rooms.

    Parameters:
        direction (str): Direction to move (north, south, east, west)

    Returns:
        None
    """
    logger.debug(f"Processing movement: {direction}")
    global current_room
    
    current_exits = GAME_WORLD[current_room]["exits"]
    if direction in current_exits:
        current_room = current_exits[direction]
        display_room(GAME_WORLD[current_room])
    else:
        print("You can't go that way!")
        logger.warning(f"Invalid direction attempted: {direction}")

def handle_inventory() -> None:
    """
    Display the player's inventory.

    Parameters:
        None

    Returns:
        None
    """
    logger.debug(f"Displaying inventory: {inventory}")
    if inventory:
        print("\nYour inventory contains:", ", ".join(inventory))
    else:
        print("\nYour inventory is empty.")

def handle_take(item: str) -> None:
    """
    Handle picking up items from the current room.

    Parameters:
        item (str): Name of the item to take

    Returns:
        None
    """
    logger.debug(f"Attempting to take item: {item}")
    if item in GAME_WORLD[current_room]["items"]:
        GAME_WORLD[current_room]["items"].remove(item)
        inventory.append(item)
        print(f"You picked up the {item}.")
        logger.info(f"Item {item} added to inventory")
    else:
        print("That item isn't here.")
        logger.warning(f"Attempted to take non-existent item: {item}")

def process_command(command: str) -> None:
    """
    Process player commands.

    Parameters:
        command (str): Player's input command

    Returns:
        None
    """
    logger.debug(f"Processing command: {command}")
    
    # Split the command into words
    words = command.lower().split()
    
    if not words:
        return
    
    action = words[0]
    
    if action in ["north", "south", "east", "west"]:
        handle_movement(action)
    elif action == "inventory":
        handle_inventory()
    elif action == "take" and len(words) > 1:
        handle_take(words[1])
    elif action == "quit":
        global game_running
        game_running = False
        print("Thanks for playing!")
    elif action == "help":
        print("\nAvailable commands:")
        print("- north, south, east, west: Move in that direction")
        print("- take [item]: Pick up an item")
        print("- inventory: Show your inventory")
        print("- quit: Exit the game")
        print("- help: Show this help message")
    else:
        print("I don't understand that command.")
        logger.warning(f"Invalid command: {command}")

def game_loop() -> None:
    """
    Main game loop.

    Parameters:
        None

    Returns:
        None
    """
    logger.info("Starting game loop")
    print("\nWelcome to the Text Adventure!")
    print('Type "help" for a list of commands.')
    
    initialize_game()
    
    while game_running:
        try:
            command = input("\nWhat would you like to do? ").strip()
            process_command(command)
        except KeyboardInterrupt:
            print("\nGame terminated by user.")
            logger.info("Game terminated by KeyboardInterrupt")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print("An error occurred. Please try again.")

if __name__ == "__main__":
    game_loop()