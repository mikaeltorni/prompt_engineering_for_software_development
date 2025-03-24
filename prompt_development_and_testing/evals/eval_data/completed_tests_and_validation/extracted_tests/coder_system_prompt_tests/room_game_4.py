"""
text_adventure.py

A simple text-based adventure game where players can navigate rooms,
collect items, and solve simple challenges.

Functions:
    initialize_game(): Sets up the initial game state
    process_command(command: str, game_state: dict): Processes player commands
    display_room(game_state: dict): Shows current room description
    handle_movement(direction: str, game_state: dict): Handles player movement
    handle_inventory(game_state: dict): Manages inventory actions
    check_win_condition(game_state: dict): Checks if player has won

Command Line Usage Example:
    python text_adventure.py
"""

import random
import time
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

def initialize_game() -> dict:
    """
    Initialize the game state with rooms, items, and player status.
    
    Parameters:
        None
        
    Returns:
        dict: Initial game state
    """
    logger.debug("Initializing new game")
    
    game_state = {
        'current_room': 'entrance',
        'inventory': [],
        'rooms': {
            'entrance': {
                'description': 'You are in the entrance hall. Dusty paintings hang on the walls.',
                'connections': {'north': 'library', 'east': 'kitchen'},
                'items': ['key']
            },
            'library': {
                'description': 'Old books line the shelves. A mysterious chest sits in the corner.',
                'connections': {'south': 'entrance', 'east': 'study'},
                'items': ['book']
            },
            'study': {
                'description': 'A cozy room with a desk and a locked drawer.',
                'connections': {'west': 'library'},
                'items': ['note']
            },
            'kitchen': {
                'description': 'A rustic kitchen with an old stove.',
                'connections': {'west': 'entrance'},
                'items': ['candle']
            }
        },
        'item_descriptions': {
            'key': 'An old brass key',
            'book': 'A dusty spellbook',
            'note': 'A mysterious note',
            'candle': 'A half-melted candle'
        }
    }
    
    logger.debug(f"Game initialized with {len(game_state['rooms'])} rooms")
    return game_state

def display_room(game_state: dict) -> None:
    """
    Display the current room description and available items.
    
    Parameters:
        game_state (dict): Current game state
        
    Returns:
        None
    """
    current_room = game_state['current_room']
    room_data = game_state['rooms'][current_room]
    
    logger.debug(f"Displaying room: {current_room}")
    
    print("\n" + "="*50)
    print(room_data['description'])
    
    if room_data['items']:
        print("\nYou see:", ", ".join(room_data['items']))
    
    print("\nPossible exits:", ", ".join(room_data['connections'].keys()))
    print("="*50)

def handle_movement(direction: str, game_state: dict) -> bool:
    """
    Handle player movement between rooms.
    
    Parameters:
        direction (str): Direction to move
        game_state (dict): Current game state
        
    Returns:
        bool: True if movement successful, False otherwise
    """
    logger.debug(f"Attempting movement: {direction}")
    
    current_room = game_state['current_room']
    connections = game_state['rooms'][current_room]['connections']
    
    if direction in connections:
        game_state['current_room'] = connections[direction]
        logger.info(f"Moved to: {game_state['current_room']}")
        return True
    else:
        print("You can't go that way!")
        logger.warning(f"Invalid movement attempted: {direction}")
        return False

def handle_inventory(command: str, game_state: dict) -> None:
    """
    Handle inventory-related actions (take, drop, view inventory).
    
    Parameters:
        command (str): Player command
        game_state (dict): Current game state
        
    Returns:
        None
    """
    logger.debug(f"Processing inventory command: {command}")
    
    if command == "inventory":
        if game_state['inventory']:
            print("\nYour inventory:", ", ".join(game_state['inventory']))
        else:
            print("\nYour inventory is empty.")
    
    elif command.startswith("take "):
        item = command[5:]
        current_room = game_state['current_room']
        room_items = game_state['rooms'][current_room]['items']
        
        if item in room_items:
            game_state['inventory'].append(item)
            room_items.remove(item)
            print(f"\nTaken: {item}")
            logger.info(f"Item taken: {item}")
        else:
            print("\nThat item isn't here.")
            logger.warning(f"Attempted to take nonexistent item: {item}")
    
    elif command.startswith("drop "):
        item = command[5:]
        if item in game_state['inventory']:
            current_room = game_state['current_room']
            game_state['inventory'].remove(item)
            game_state['rooms'][current_room]['items'].append(item)
            print(f"\nDropped: {item}")
            logger.info(f"Item dropped: {item}")
        else:
            print("\nYou don't have that item.")
            logger.warning(f"Attempted to drop nonexistent item: {item}")

def process_command(command: str, game_state: dict) -> bool:
    """
    Process player commands.
    
    Parameters:
        command (str): Player command
        game_state (dict): Current game state
        
    Returns:
        bool: False if game should end, True otherwise
    """
    logger.debug(f"Processing command: {command}")
    
    command = command.lower().strip()
    
    if command in ["quit", "exit"]:
        return False
    
    elif command in ["north", "south", "east", "west"]:
        handle_movement(command, game_state)
    
    elif command in ["inventory", "i"] or command.startswith(("take ", "drop ")):
        handle_inventory(command, game_state)
    
    elif command == "look":
        display_room(game_state)
    
    elif command == "help":
        print("\nAvailable commands:")
        print("- north, south, east, west: Move in that direction")
        print("- take <item>: Pick up an item")
        print("- drop <item>: Drop an item")
        print("- inventory: Show your inventory")
        print("- look: Look around")
        print("- quit: Exit the game")
    
    else:
        print("\nI don't understand that command. Type 'help' for commands.")
        logger.warning(f"Invalid command: {command}")
    
    return True

def main():
    """
    Main game loop.
    
    Parameters:
        None
        
    Returns:
        None
    """
    print("\nWelcome to the Text Adventure!")
    print("Type 'help' for commands.")
    
    game_state = initialize_game()
    
    while True:
        display_room(game_state)
        
        try:
            command = input("\nWhat would you like to do? ").strip()
            if not process_command(command, game_state):
                print("\nThanks for playing!")
                break
                
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print("\nAn error occurred. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        logger.info("Game terminated by user")
        sys.exit(0)