"""
Test script to verify critical hit system
"""

import random
from pokemon import Pokemon
from move import Move
from battle import calculate_damage

# Set seed for reproducible test
random.seed(42)

# Create test Pokemon and move
pikachu = Pokemon("Pikachu", "Electric", 35, 55, 40, 90)
charmander = Pokemon("Charmander", "Fire", 39, 52, 43, 65)
thunderbolt = Move("Thunderbolt", "Electric", 90, 100)

print("=== Critical Hit System Test ===\n")
print("Testing 20 attacks to demonstrate critical hit system (10% chance):\n")

critical_count = 0
for i in range(20):
    damage, effectiveness, is_critical = calculate_damage(pikachu, charmander, thunderbolt)
    
    status = "CRITICAL HIT!" if is_critical else "Normal"
    print(f"Attack {i+1}: {damage} damage - {status}")
    
    if is_critical:
        critical_count += 1

print(f"\nTotal critical hits: {critical_count}/20 ({critical_count/20*100:.1f}%)")
print("Expected: ~2/20 (10%)")
print("\n=== Test Complete ===")
