"""
Pokemon Battle Game - Move System
A simple Move class representing Pokemon attacks
"""


class Move:
    """
    Represents a Pokemon move/attack.
    
    Attributes:
        name (str): The move's name
        type (str): The move's type (e.g., 'Fire', 'Water', 'Electric')
        power (int): The move's base power
        accuracy (int): Hit chance percentage (0-100)
    """
    
    def __init__(self, name, type, power, accuracy):
        """
        Initialize a new Move.
        
        Args:
            name (str): Move's name
            type (str): Move's type
            power (int): Base power of the move
            accuracy (int): Accuracy percentage (0-100)
        """
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy
    
    def show_info(self):
        """
        Display the move's information in a clear format.
        Shows name, type, power, and accuracy.
        """
        print(f"{self.name} ({self.type})")
        print(f"  Power: {self.power}")
        print(f"  Accuracy: {self.accuracy}%")


# ============================================
# TEST SECTION
# ============================================
if __name__ == "__main__":
    print("=== Pokemon Move System - Test ===\n")
    
    # Create different types of moves
    thunderbolt = Move(
        name="Thunderbolt",
        type="Electric",
        power=90,
        accuracy=100
    )
    
    flamethrower = Move(
        name="Flamethrower",
        type="Fire",
        power=90,
        accuracy=100
    )
    
    hydro_pump = Move(
        name="Hydro Pump",
        type="Water",
        power=110,
        accuracy=80
    )
    
    # Display all moves
    print("Move 1:")
    thunderbolt.show_info()
    
    print("\nMove 2:")
    flamethrower.show_info()
    
    print("\nMove 3:")
    hydro_pump.show_info()
    
    print("\n=== Test Complete ===")
