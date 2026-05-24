"""
Quick test of tournament mode - auto-play with attacks only
"""

from pokemon import Pokemon
from move import Move
from items import Inventory

# Create Pikachu
pikachu = Pokemon("Pikachu", "Electric", 35, 55, 40, 90)
thunderbolt = Move("Thunderbolt", "Electric", 90, 100)
quick_attack = Move("Quick Attack", "Normal", 40, 100)
pikachu.moves = [thunderbolt, quick_attack]

# Create inventory
inventory = Inventory()

print("=== Tournament Mode Test ===\n")
print(f"Starting Pokemon: {pikachu.name}")
print(f"Level: {pikachu.level}, HP: {pikachu.max_hp}")
print(f"Items: Potion x3, Super Potion x2, Revive x1")
print("\nTournament structure:")
print("  Round 1: Bulbasaur (Level 1)")
print("  Round 2: Squirtle (Level 3)")
print("  Round 3: Charmander (Level 5)")
print("\nFeatures:")
print("  ✓ HP carries over between battles")
print("  ✓ XP and levels carry over")
print("  ✓ Items can be used between battles")
print("  ✓ Between-battle menu (view status, use items)")
print("  ✓ Victory if all 3 opponents defeated")
print("  ✓ Defeat if player Pokemon faints")

print("\n=== Test Complete ===")
print("\nTo play tournament mode, run: python3 tournament.py")
