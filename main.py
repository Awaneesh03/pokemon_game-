"""
Pokemon Battle Game - Main Integration
Connects Pokemon and Move classes to create battle-ready Pokemon
"""

from pokemon import Pokemon
from move import Move


def main():
    """
    Main function to demonstrate Pokemon with moves.
    """
    print("=== Pokemon Battle Game - Integration Test ===\n")
    
    # ============================================
    # CREATE MOVES
    # ============================================
    thunderbolt = Move(
        name="Thunderbolt",
        type="Electric",
        power=90,
        accuracy=100
    )
    
    quick_attack = Move(
        name="Quick Attack",
        type="Normal",
        power=40,
        accuracy=100
    )
    
    ember = Move(
        name="Ember",
        type="Fire",
        power=40,
        accuracy=100
    )
    
    scratch = Move(
        name="Scratch",
        type="Normal",
        power=40,
        accuracy=100
    )
    
    # ============================================
    # CREATE POKEMON
    # ============================================
    pikachu = Pokemon(
        name="Pikachu",
        type="Electric",
        max_hp=35,
        attack=55,
        defense=40,
        speed=90
    )
    
    charmander = Pokemon(
        name="Charmander",
        type="Fire",
        max_hp=39,
        attack=52,
        defense=43,
        speed=65
    )
    
    # ============================================
    # ASSIGN MOVES TO POKEMON
    # ============================================
    pikachu.moves = [thunderbolt, quick_attack]
    charmander.moves = [ember, scratch]
    
    # ============================================
    # DISPLAY POKEMON AND THEIR MOVES
    # ============================================
    print("--- Pikachu ---")
    pikachu.show_status()
    print(f"Type: {pikachu.type}")
    pikachu.show_moves()
    
    print("\n--- Charmander ---")
    charmander.show_status()
    print(f"Type: {charmander.type}")
    charmander.show_moves()
    
    print("\n=== Integration Test Complete ===")


if __name__ == "__main__":
    main()
