"""
Test script to verify XP and leveling system
"""

from pokemon import Pokemon
from move import Move

print("=== XP and Leveling System Test ===\n")

# Create a test Pokemon
pikachu = Pokemon("Pikachu", "Electric", 35, 55, 40, 90)
thunderbolt = Move("Thunderbolt", "Electric", 90, 100)
pikachu.moves = [thunderbolt]

print("Initial stats:")
print(f"Level: {pikachu.level}")
print(f"XP: {pikachu.xp}")
print(f"HP: {pikachu.max_hp}, ATK: {pikachu.attack}, DEF: {pikachu.defense}, SPD: {pikachu.speed}")

# Test 1: Gain 50 XP (not enough to level up)
print("\n--- Test 1: Gain 50 XP ---")
pikachu.gain_xp(50)
print(f"Current: Level {pikachu.level}, XP: {pikachu.xp}/100")

# Test 2: Gain 50 more XP (should level up to 2)
print("\n--- Test 2: Gain 50 more XP (total 100) ---")
pikachu.gain_xp(50)
print(f"Current: Level {pikachu.level}, XP: {pikachu.xp}/200")

# Test 3: Gain 200 XP (should level up to 3)
print("\n--- Test 3: Gain 200 XP ---")
pikachu.gain_xp(200)
print(f"Current: Level {pikachu.level}, XP: {pikachu.xp}/300")

# Test 4: Gain 1000 XP (multiple level-ups)
print("\n--- Test 4: Gain 1000 XP (multiple level-ups) ---")
pikachu.gain_xp(1000)
print(f"Final: Level {pikachu.level}, XP: {pikachu.xp}/{pikachu.level * 100}")

print("\n=== Test Complete ===")
