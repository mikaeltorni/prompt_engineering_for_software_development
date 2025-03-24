class Game:
    def __init__(self):
        self.current_room = "hall"
        self.inventory = []
        self.game_over = False
        
        # Define rooms and their connections
        self.rooms = {
            "hall": {
                "description": "You are in a dimly lit hall. There's a strange smell in the air.",
                "connections": {"north": "kitchen", "east": "study"},
                "items": ["key"],
            },
            "kitchen": {
                "description": "You're in a messy kitchen. Dishes are piled up in the sink.",
                "connections": {"south": "hall", "east": "garden"},
                "items": ["knife"],
            },
            "study": {
                "description": "A cozy study with books scattered everywhere.",
                "connections": {"west": "hall"},
                "items": ["book"],
            },
            "garden": {
                "description": "A beautiful garden with mysterious plants.",
                "connections": {"west": "kitchen"},
                "items": ["flower"],
                "requires": "key"  # Need key to enter
            }
        }

    def show_status(self):
        """Display current room and inventory"""
        room = self.rooms[self.current_room]
        print("\n" + "=" * 50)
        print(f"You are in the {self.current_room}")
        print(room["description"])
        
        # Show items in room
        if room["items"]:
            print("\nYou see:", ", ".join(room["items"]))
            
        # Show possible directions
        print("\nPossible directions:", ", ".join(room["connections"].keys()))
        
        # Show inventory
        print("\nInventory:", ", ".join(self.inventory) if self.inventory else "empty")
        print("=" * 50)

    def get_command(self):
        """Get player command"""
        return input("\nWhat would you like to do? ").lower().split()

    def move(self, direction):
        """Move to another room"""
        room = self.rooms[self.current_room]
        
        if direction in room["connections"]:
            new_room = room["connections"][direction]
            
            # Check if room requires an item
            if "requires" in self.rooms[new_room]:
                required_item = self.rooms[new_room]["requires"]
                if required_item not in self.inventory:
                    print(f"\nYou need a {required_item} to enter this room!")
                    return
                
            self.current_room = new_room
            print(f"\nYou move {direction} to the {new_room}")
        else:
            print("\nYou can't go that way!")

    def take_item(self, item):
        """Pick up an item"""
        room = self.rooms[self.current_room]
        
        if item in room["items"]:
            room["items"].remove(item)
            self.inventory.append(item)
            print(f"\nYou picked up the {item}")
        else:
            print("\nThat item isn't here!")

    def play(self):
        """Main game loop"""
        print("\nWelcome to the Adventure Game!")
        print("Commands: go [direction], take [item], inventory, quit")
        
        while not self.game_over:
            self.show_status()
            command = self.get_command()
            
            if not command:
                continue
                
            action = command[0]
            
            if action == "quit":
                print("\nThanks for playing!")
                self.game_over = True
                
            elif action == "go" and len(command) > 1:
                self.move(command[1])
                
            elif action == "take" and len(command) > 1:
                self.take_item(command[1])
                
            elif action == "inventory":
                print("\nInventory:", ", ".join(self.inventory) if self.inventory else "empty")
                
            else:
                print("\nI don't understand that command.")
                print("Commands: go [direction], take [item], inventory, quit")

# Start the game
if __name__ == "__main__":
    game = Game()
    game.play()