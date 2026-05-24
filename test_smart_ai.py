"""
Test smart AI system
"""

from pokemon import Pokemon
from move import Move
from battle import choose_best_move, get_type_effectiveness

print("=== Smart AI System Test ===\n")

# Create test Pokemon
pikachu = Pokemon("Pikachu", "Electric", 35, 55, 40, 90)
squirtle = Pokemon("Squirtle", "Water", 44, 48, 65, 43)

# Create moves for Squirtle
water_gun = Move("Water Gun", "Water", 40, 100)  # Not effective vs Electric
tackle = Move("Tackle", "Normal", 40, 100)  # Neutral
hydro_pump = Move("Hydro Pump", "Water", 110, 80)  # Not effective but high power

squirtle.moves = [water_gun, tackle, hydro_pump]

print("Test Scenario:")
print(f"  Attacker: {squirtle.name} (Water type)")
print(f"  Defender: {pikachu.name} (Electric type)")
print(f"\nAvailable moves:")
for move in squirtle.moves:
    effectiveness = get_type_effectiveness(move.type, pikachu.type)
    print(f"  - {move.name} ({move.type}): Power {move.power}, Effectiveness {effectiveness}x")

print("\n--- Testing AI Decision Making ---")
print("Running 10 AI move selections:\n")

move_counts = {}
for i in range(10):
    chosen = choose_best_move(squirtle, pikachu)
    move_counts[chosen.name] = move_counts.get(chosen.name, 0) + 1
    
    effectiveness = get_type_effectiveness(chosen.type, pikachu.type)
    expected_damage = (chosen.power + squirtle.attack - pikachu.defense) * effectiveness
    print(f"  {i+1}. Chose: {chosen.name} (Expected damage: {expected_damage:.1f})")

print("\n--- Move Selection Summary ---")
for move_name, count in sorted(move_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {move_name}: {count}/10 times ({count*10}%)")

print("\n--- Expected AI Behavior ---")
print("  ✓ Should prefer Tackle (neutral, consistent damage)")
print("  ✓ Should avoid Water moves (not effective vs Electric)")
print("  ✓ 15% randomness means occasional suboptimal choices")

print("\n=== Test Complete ===")
