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
                "items": ["treasure"],
                "requirements": "key"
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
        """Move to a different room"""
        room = self.rooms[self.current_room]
        
        if direction in room["connections"]:
            next_room = room["connections"][direction]
            
            # Check if room has requirements
            if self.rooms[next_room]["requirements"]:
                required_item = self.rooms[next_room]["requirements"]
                if required_item not in self.inventory:
                    print(f"\nYou need a {required_item} to enter this room!")
                    return
                    
            self.current_room = next_room
            print(f"\nYou move to the {next_room}")
        else:
            print("\nYou can't go that way!")

    def take_item(self, item):
        """Pick up an item"""
        room = self.rooms[self.current_room]
        
        if item in room["items"]:
            self.inventory.append(item)
            room["items"].remove(item)
            print(f"\nYou picked up the {item}")
            
            # Win condition
            if item == "treasure":
                print("\nCongratulations! You found the treasure! You win!")
                self.game_over = True
        else:
            print("\nThat item isn't here!")

    def play(self):
        """Main game loop"""
        print("\nWelcome to the Adventure Game!")
        print("Commands: 'go [direction]', 'take [item]', 'quit'")
        
        while not self.game_over:
            self.show_status()
            command = self.get_command()
            
            if not command:
                continue
                
            action = command[0]
            
            if action == "quit":
                print("\nThanks for playing!")
                break
                
            if len(command) < 2:
                print("\nIncomplete command!")
                continue
                
            if action == "go":
                self.move(command[1])
            elif action == "take":
                self.take_item(command[1])
            else:
                print("\nInvalid command!")

# Start the game
if __name__ == "__main__":
    game = Game()
    game.play()