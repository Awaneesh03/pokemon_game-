"""
Test move unlock system
"""

from pokemon import Pokemon
from move import Move
from learnsets import get_starting_moves, get_moves_at_level

print("=== Move Unlock System Test ===\n")

# Create Pikachu
pikachu = Pokemon("Pikachu", "Electric", 35, 55, 40, 90)

# Get starting moves
starting_moves = get_starting_moves("Pikachu")
pikachu.moves = starting_moves

print("Initial state:")
print(f"  {pikachu.name} - Level {pikachu.level}")
print(f"  Moves: {[m.name for m in pikachu.moves]}")

# Test leveling up to level 5 (should learn Iron Tail)
print("\n--- Gaining XP to reach Level 5 ---")
pikachu.gain_xp(400, is_player=False)  # AI mode for auto-testing

print("\n--- Final state ---")
print(f"  {pikachu.name} - Level {pikachu.level}")
print(f"  Moves: {[m.name for m in pikachu.moves]}")

print("\n--- Expected Behavior ---")
print("  ✓ Should start with Quick Attack and Thunderbolt")
print("  ✓ Should learn Iron Tail at level 5")
print("  ✓ AI should auto-replace weakest move if at 4-move limit")

print("\n=== Test Complete ===")
