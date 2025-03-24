class Game:
    def __init__(self):
        self.inventory = []
        self.current_room = "hall"
        
        # Define rooms and their connections
        self.rooms = {
            "hall": {
                "description": "You are in a dimly lit hall. There's a kitchen to the north and a bedroom to the east.",
                "connections": {"north": "kitchen", "east": "bedroom"},
                "items": ["key"]
            },
            "kitchen": {
                "description": "You're in a messy kitchen. There's a hall to the south and a garden to the east.",
                "connections": {"south": "hall", "east": "garden"},
                "items": ["knife", "apple"]
            },
            "bedroom": {
                "description": "You're in a cozy bedroom. There's a hall to the west and a garden to the north.",
                "connections": {"west": "hall", "north": "garden"},
                "items": ["book"]
            },
            "garden": {
                "description": "You're in a beautiful garden. There's a kitchen to the west and a bedroom to the south.",
                "connections": {"west": "kitchen", "south": "bedroom"},
                "items": ["flower"],
                "locked": True
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
        print("\nInventory:", self.inventory if self.inventory else "Empty")
        print("="*50)

    def move(self, direction):
        """Move to a different room"""
        if direction in self.rooms[self.current_room]["connections"]:
            next_room = self.rooms[self.current_room]["connections"][direction]
            
            # Check if room is locked
            if "locked" in self.rooms[next_room] and self.rooms[next_room]["locked"]:
                if "key" in self.inventory:
                    print("\nYou use the key to unlock the door.")
                    self.rooms[next_room]["locked"] = False
                else:
                    print("\nThe door is locked! You need a key.")
                    return
                    
            self.current_room = next_room
            print(f"\nYou move {direction} to the {next_room}.")
        else:
            print("\nYou can't go that way!")

    def take_item(self, item):
        """Pick up an item from the current room"""
        if item in self.rooms[self.current_room]["items"]:
            self.rooms[self.current_room]["items"].remove(item)
            self.inventory.append(item)
            print(f"\nYou picked up the {item}.")
        else:
            print("\nThat item isn't here!")

    def drop_item(self, item):
        """Drop an item in the current room"""
        if item in self.inventory:
            self.inventory.remove(item)
            self.rooms[self.current_room]["items"].append(item)
            print(f"\nYou dropped the {item}.")
        else:
            print("\nYou don't have that item!")

def main():
    game = Game()
    print("\nWelcome to the Adventure Game!")
    print("Commands: go [direction], take [item], drop [item], inventory, quit")
    
    while True:
        game.show_status()
        
        command = input("\nWhat would you like to do? ").lower().split()
        
        if not command:
            continue
            
        if command[0] == "quit":
            print("\nThanks for playing!")
            break
            
        if command[0] == "go" and len(command) > 1:
            game.move(command[1])
            
        elif command[0] == "take" and len(command) > 1:
            game.take_item(command[1])
            
        elif command[0] == "drop" and len(command) > 1:
            game.drop_item(command[1])
            
        elif command[0] == "inventory":
            print("\nInventory:", game.inventory if game.inventory else "Empty")
            
        else:
            print("\nInvalid command! Try: go [direction], take [item], drop [item], inventory, quit")

if __name__ == "__main__":
    main()