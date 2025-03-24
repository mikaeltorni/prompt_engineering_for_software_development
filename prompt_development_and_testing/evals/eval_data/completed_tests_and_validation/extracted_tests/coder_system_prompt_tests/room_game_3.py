"""
text_adventure.py

A simple text-based adventure game where players can explore rooms,
collect items, and solve simple challenges.

Functions:
    initialize_game(): Sets up the game world
    play_game(): Main game loop
    process_command(command: str, player: Player): Processes player commands
    display_help(): Shows available commands

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
        self.challenge_solved = False
        logger.debug(f"Created room: {name}")

class Player:
    """
    Represents the player character.
    
    Parameters:
        starting_room (Room): The room where the player starts
        
    Returns:
        None
    """
    def __init__(self, starting_room: Room):
        self.current_room = starting_room
        self.inventory: List[str] = []
        logger.debug("Player initialized")

def initialize_game() -> Player:
    """
    Sets up the game world with rooms, items, and challenges.
    
    Parameters:
        None
        
    Returns:
        Player: Initialized player object in starting room
    """
    logger.debug("Initializing game world")
    
    # Create rooms
    entrance = Room("Entrance Hall", "A grand entrance hall with marble floors.")
    library = Room("Library", "A dusty library filled with ancient books.")
    kitchen = Room("Kitchen", "A medieval kitchen with a large fireplace.")
    cellar = Room("Cellar", "A dark cellar with mysterious barrels.")
    
    # Connect rooms
    entrance.connections = {"north": library, "east": kitchen}
    library.connections = {"south": entrance, "east": cellar}
    kitchen.connections = {"west": entrance, "north": cellar}
    cellar.connections = {"west": library, "south": kitchen}
    
    # Add items
    entrance.items = ["key"]
    library.items = ["book"]
    kitchen.items = ["knife"]
    cellar.items = ["potion"]
    
    # Add challenges
    library.challenge = "What has pages but no words?"
    library.challenge_answer = "book"
    
    logger.debug("Game world initialized")
    return Player(entrance)

def display_help() -> None:
    """
    Displays available commands to the player.
    
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
    print("- solve <answer>: Solve a room's challenge")
    print("- help: Show this help message")
    print("- quit: Exit the game")

def process_command(command: str, player: Player) -> bool:
    """
    Processes player commands and updates game state.
    
    Parameters:
        command (str): Player's input command
        player (Player): Current player object
        
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
            print(f"\nYou are in the {player.current_room.name}")
            print(player.current_room.description)
            if player.current_room.items:
                print(f"You see: {', '.join(player.current_room.items)}")
            if player.current_room.challenge and not player.current_room.challenge_solved:
                print(f"There's a challenge here: {player.current_room.challenge}")
            print("Exits:", ", ".join(player.current_room.connections.keys()))
            
        elif action == "inventory":
            if player.inventory:
                print("You are carrying:", ", ".join(player.inventory))
            else:
                print("Your inventory is empty.")
                
        elif action == "go":
            if len(words) < 2:
                print("Go where? Please specify a direction.")
                return True
                
            direction = words[1]
            if direction in player.current_room.connections:
                player.current_room = player.current_room.connections[direction]
                print(f"\nYou move to the {player.current_room.name}")
            else:
                print("You can't go that way!")
                
        elif action == "take":
            if len(words) < 2:
                print("Take what? Please specify an item.")
                return True
                
            item = words[1]
            if item in player.current_room.items:
                player.current_room.items.remove(item)
                player.inventory.append(item)
                print(f"You take the {item}.")
            else:
                print("You don't see that here.")
                
        elif action == "solve":
            if len(words) < 2:
                print("Solve what? Please provide an answer.")
                return True
                
            if not player.current_room.challenge:
                print("There's no challenge to solve here.")
            elif player.current_room.challenge_solved:
                print("You've already solved this challenge!")
            else:
                answer = words[1]
                if answer == player.current_room.challenge_answer:
                    print("Correct! You solved the challenge!")
                    player.current_room.challenge_solved = True
                else:
                    print("That's not the correct answer.")
                    
        else:
            print("I don't understand that command. Type 'help' for available commands.")
            
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
    logger.info("Starting new game")
    
    print("\nWelcome to the Text Adventure!")
    print("Type 'help' for a list of commands.")
    
    player = initialize_game()
    running = True
    
    while running:
        try:
            command = input("\nWhat would you like to do? ").strip()
            running = process_command(command, player)
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
        sys.exit(1)