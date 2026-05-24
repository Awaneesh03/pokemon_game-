"""
Test script for items in battle
"""

from pokemon import Pokemon
from move import Move
from battle import battle
from items import Inventory

print("=== Items in Battle Test ===\n")

# Create moves
quick_attack = Move("Quick Attack", "Normal", 40, 100)
scratch = Move("Scratch", "Normal", 40, 100)

# Create Pokemon - make them weaker for longer battle
pikachu = Pokemon("Pikachu", "Electric", 50, 30, 30, 90)
pikachu.moves = [quick_attack]

charmander = Pokemon("Charmander", "Fire", 50, 30, 30, 65)
charmander.moves = [scratch]

# Create inventory
inventory = Inventory()

print("Starting battle with items enabled!")
print("Try using items during battle (choose option 2)\n")

# Start battle
battle(pikachu, charmander, inventory)

print("\n=== Test Complete ===")
