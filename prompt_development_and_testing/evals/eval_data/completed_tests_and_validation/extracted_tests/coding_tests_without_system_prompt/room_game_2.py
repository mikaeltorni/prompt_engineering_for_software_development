class Game:
    def __init__(self):
        self.inventory = []
        self.current_room = "hall"
        self.game_over = False
        
        # Define rooms and their connections
        self.rooms = {
            "hall": {
                "description": "You are in a dimly lit hall. There's a strange smell in the air.",
                "connections": {"north": "kitchen", "east": "library"},
                "items": ["key"],
                "requirements": None
            },
            "kitchen": {
                "description": "A messy kitchen with dirty dishes everywhere.",
                "connections": {"south": "hall", "east": "garden"},
                "items": ["knife"],
                "requirements": None
            },
            "library": {
                "description": "Dusty bookshelves line the walls.",
                "connections": {"west": "hall", "north": "garden"},
                "items": ["book"],
                "requirements": None
            },
            "garden": {
                "description": "A beautiful garden with a locked chest.",
                "connections": {"west": "kitchen", "south": "library"},
                "items": ["chest"],
                "requirements": {"chest": "key"}
            }
        }

    def show_status(self):
        """Display current room and inventory"""
        room = self.rooms[self.current_room]
        print("\n" + "=" * 50)
        print(f"You are in the {self.current_room}")
        print(room["description"])
        
        if room["items"]:
            print("\nYou see:", ", ".join(room["items"]))
            
        print("\nPossible directions:", ", ".join(room["connections"].keys()))
        print("\nInventory:", ", ".join(self.inventory) if self.inventory else "Empty")
        print("=" * 50)

    def get_command(self):
        """Get player command"""
        return input("\nWhat would you like to do? ").lower().split()

    def move(self, direction):
        """Move player to another room"""
        room = self.rooms[self.current_room]
        if direction in room["connections"]:
            self.current_room = room["connections"][direction]
            return True
        else:
            print("You can't go that way!")
            return False

    def take(self, item):
        """Pick up an item"""
        room = self.rooms[self.current_room]
        if item in room["items"]:
            if item == "chest":
                if "key" in self.inventory:
                    print("You unlocked the chest! You win!")
                    self.game_over = True
                else:
                    print("The chest is locked! You need a key.")
                return
            room["items"].remove(item)
            self.inventory.append(item)
            print(f"Picked up {item}")
        else:
            print("Can't find that item!")

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
                print("Thanks for playing!")
                break
                
            elif action == "go" and len(command) > 1:
                self.move(command[1])
                
            elif action == "take" and len(command) > 1:
                self.take(command[1])
                
            elif action == "inventory":
                print("\nInventory:", ", ".join(self.inventory) if self.inventory else "Empty")
                
            else:
                print("Invalid command! Try: go [direction], take [item], inventory, quit")

# Start the game
if __name__ == "__main__":
    game = Game()
    game.play()