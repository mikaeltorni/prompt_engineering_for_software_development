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
                "examined": False
            },
            "kitchen": {
                "description": "You're in a messy kitchen. Dishes are piled up in the sink.",
                "connections": {"south": "hall", "east": "garden"},
                "items": ["knife"],
                "examined": False
            },
            "study": {
                "description": "A cozy study with a large desk and bookshelf.",
                "connections": {"west": "hall", "north": "garden"},
                "items": ["book"],
                "examined": False
            },
            "garden": {
                "description": "A beautiful garden with a locked chest.",
                "connections": {"west": "kitchen", "south": "study"},
                "items": ["flower"],
                "examined": False,
                "requires": "key"
            }
        }

    def show_status(self):
        """Display current room and inventory"""
        room = self.rooms[self.current_room]
        print("\n" + "=" * 50)
        print(f"You are in the {self.current_room}")
        print(room["description"])
        
        if room["items"]:
            print("\nYou see the following items:")
            for item in room["items"]:
                print(f"- {item}")
                
        print("\nPossible directions:")
        for direction in room["connections"]:
            print(f"- {direction}")
            
        print("\nInventory:", self.inventory)
        print("=" * 50)

    def get_command(self):
        """Get player command"""
        return input("\nWhat would you like to do? ").lower().split()

    def move(self, direction):
        """Move player to another room"""
        room = self.rooms[self.current_room]
        
        if direction in room["connections"]:
            next_room = room["connections"][direction]
            
            # Check if room requires an item
            if "requires" in self.rooms[next_room]:
                required_item = self.rooms[next_room]["requires"]
                if required_item not in self.inventory:
                    print(f"\nYou need a {required_item} to enter this room!")
                    return
                    
            self.current_room = next_room
            print(f"\nYou move {direction} to the {next_room}")
        else:
            print("\nYou can't go that way!")

    def take(self, item):
        """Pick up an item"""
        room = self.rooms[self.current_room]
        
        if item in room["items"]:
            room["items"].remove(item)
            self.inventory.append(item)
            print(f"\nYou picked up the {item}")
        else:
            print("\nThat item isn't here!")

    def examine(self):
        """Examine the current room"""
        room = self.rooms[self.current_room]
        
        if not room["examined"]:
            if self.current_room == "garden" and "key" in self.inventory:
                print("\nYou use the key to open the chest and find a golden crown! You win!")
                self.game_over = True
            else:
                print("\nYou find nothing special.")
            room["examined"] = True
        else:
            print("\nYou've already examined this room.")

    def play(self):
        """Main game loop"""
        print("\nWelcome to the Adventure Game!")
        print("Commands: go [direction], take [item], examine, inventory, quit")
        
        while not self.game_over:
            self.show_status()
            command = self.get_command()
            
            if not command:
                continue
                
            action = command[0]
            
            if action == "quit":
                print("\nThanks for playing!")
                break
                
            elif action == "go" and len(command) > 1:
                self.move(command[1])
                
            elif action == "take" and len(command) > 1:
                self.take(command[1])
                
            elif action == "examine":
                self.examine()
                
            elif action == "inventory":
                print("\nYour inventory:", self.inventory)
                
            else:
                print("\nInvalid command! Try: go [direction], take [item], examine, inventory, quit")

# Start the game
if __name__ == "__main__":
    game = Game()
    game.play()