class Game:
    def __init__(self):
        self.inventory = []
        self.current_room = "hall"
        
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
                "items": ["knife", "apple"],
            },
            "study": {
                "description": "A cozy study with books scattered everywhere.",
                "connections": {"west": "hall", "north": "garden"},
                "items": ["book"],
            },
            "garden": {
                "description": "A beautiful garden with mysterious plants.",
                "connections": {"west": "kitchen", "south": "study"},
                "items": ["flower"],
            }
        }

    def show_status(self):
        """Display current room and inventory"""
        print("\n" + "="*50)
        print(f"You are in the {self.current_room}")
        print(self.rooms[self.current_room]["description"])
        
        # Show items in room
        if self.rooms[self.current_room]["items"]:
            print("\nYou see the following items:")
            for item in self.rooms[self.current_room]["items"]:
                print(f"- {item}")
        
        # Show possible directions
        print("\nPossible directions:")
        for direction in self.rooms[self.current_room]["connections"]:
            print(f"- {direction}")
        
        # Show inventory
        print("\nInventory:")
        if self.inventory:
            for item in self.inventory:
                print(f"- {item}")
        else:
            print("Empty")
        print("="*50)

    def move(self, direction):
        """Move to a different room"""
        if direction in self.rooms[self.current_room]["connections"]:
            self.current_room = self.rooms[self.current_room]["connections"][direction]
            return True
        else:
            print("\nYou can't go that way!")
            return False

    def take_item(self, item):
        """Pick up an item from the current room"""
        if item in self.rooms[self.current_room]["items"]:
            self.rooms[self.current_room]["items"].remove(item)
            self.inventory.append(item)
            print(f"\nYou picked up the {item}")
        else:
            print("\nThat item isn't here!")

    def drop_item(self, item):
        """Drop an item in the current room"""
        if item in self.inventory:
            self.inventory.remove(item)
            self.rooms[self.current_room]["items"].append(item)
            print(f"\nYou dropped the {item}")
        else:
            print("\nYou don't have that item!")

def main():
    game = Game()
    print("\nWelcome to the Adventure Game!")
    print("Commands: 'go [direction]', 'take [item]', 'drop [item]', 'inventory', 'quit'")
    
    while True:
        game.show_status()
        
        command = input("\nWhat would you like to do? ").lower().split()
        
        if not command:
            continue
            
        if command[0] == "quit":
            print("\nThanks for playing!")
            break
            
        elif command[0] == "go":
            if len(command) < 2:
                print("\nGo where?")
                continue
            game.move(command[1])
            
        elif command[0] == "take":
            if len(command) < 2:
                print("\nTake what?")
                continue
            game.take_item(command[1])
            
        elif command[0] == "drop":
            if len(command) < 2:
                print("\nDrop what?")
                continue
            game.drop_item(command[1])
            
        elif command[0] == "inventory":
            print("\nYour inventory:")
            for item in game.inventory:
                print(f"- {item}")
                
        else:
            print("\nI don't understand that command.")

if __name__ == "__main__":
    main()