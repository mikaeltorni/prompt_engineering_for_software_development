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
                "description": "You're in a messy kitchen. Dishes are piled up everywhere.",
                "connections": {"south": "hall", "east": "garden"},
                "items": ["knife"],
                "examined": False
            },
            "study": {
                "description": "A cozy study with a large desk and many books.",
                "connections": {"west": "hall", "north": "garden"},
                "items": ["book"],
                "examined": False
            },
            "garden": {
                "description": "A beautiful garden with a mysterious locked chest.",
                "connections": {"west": "kitchen", "south": "study"},
                "items": ["flower"],
                "examined": False,
                "requires": "key"
            }
        }

    def show_room(self):
        """Display current room description and available directions"""
        room = self.rooms[self.current_room]
        if not room["examined"]:
            print("\n" + room["description"])
            room["examined"] = True
        
        print("\nAvailable directions:", list(room["connections"].keys()))
        if room["items"]:
            print("Items in room:", room["items"])

    def move(self, direction):
        """Move player to a new room"""
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
            print(f"\nMoving {direction}...")
            self.show_room()
        else:
            print("\nYou can't go that way!")

    def take(self, item):
        """Pick up an item from the current room"""
        room = self.rooms[self.current_room]
        if item in room["items"]:
            room["items"].remove(item)
            self.inventory.append(item)
            print(f"\nPicked up {item}")
        else:
            print("\nThat item isn't here!")

    def show_inventory(self):
        """Display player's inventory"""
        if self.inventory:
            print("\nInventory:", self.inventory)
        else:
            print("\nYour inventory is empty")

    def play(self):
        """Main game loop"""
        print("\nWelcome to the Adventure Game!")
        print("Commands: north, south, east, west, take [item], inventory, quit")
        
        self.show_room()

        while not self.game_over:
            command = input("\nWhat would you like to do? ").lower().split()
            
            if not command:
                continue
                
            if command[0] in ["north", "south", "east", "west"]:
                self.move(command[0])
            elif command[0] == "take" and len(command) > 1:
                self.take(command[1])
            elif command[0] == "inventory":
                self.show_inventory()
            elif command[0] == "quit":
                print("\nThanks for playing!")
                self.game_over = True
            else:
                print("\nI don't understand that command")

# Start the game
if __name__ == "__main__":
    game = Game()
    game.play()