"""
Pokemon Battle Game - Move Learnsets
Defines which moves Pokemon learn at which levels
"""

from move import Move


# Define all moves
THUNDERBOLT = Move("Thunderbolt", "Electric", 90, 100)
QUICK_ATTACK = Move("Quick Attack", "Normal", 40, 100)
THUNDER = Move("Thunder", "Electric", 110, 70)
IRON_TAIL = Move("Iron Tail", "Normal", 100, 75)

EMBER = Move("Ember", "Fire", 40, 100)
SCRATCH = Move("Scratch", "Normal", 40, 100)
FLAMETHROWER = Move("Flamethrower", "Fire", 90, 100)
METAL_CLAW = Move("Metal Claw", "Normal", 50, 95)
FIRE_BLAST = Move("Fire Blast", "Fire", 110, 85)

WATER_GUN = Move("Water Gun", "Water", 40, 100)
TACKLE = Move("Tackle", "Normal", 40, 100)
BUBBLE_BEAM = Move("Bubble Beam", "Water", 65, 100)
BITE = Move("Bite", "Normal", 60, 100)
HYDRO_PUMP = Move("Hydro Pump", "Water", 110, 80)

VINE_WHIP = Move("Vine Whip", "Grass", 45, 100)
RAZOR_LEAF = Move("Razor Leaf", "Grass", 55, 95)
SOLAR_BEAM = Move("Solar Beam", "Grass", 120, 100)


# Learnsets: {pokemon_name: {level: [Move, ...]}}
LEARNSETS = {
    "Pikachu": {
        1: [QUICK_ATTACK, THUNDERBOLT],  # Starting moves
        5: [IRON_TAIL],
        10: [THUNDER]
    },
    "Charmander": {
        1: [SCRATCH, EMBER],  # Starting moves
        7: [METAL_CLAW],
        13: [FLAMETHROWER],
        20: [FIRE_BLAST]
    },
    "Squirtle": {
        1: [TACKLE, WATER_GUN],  # Starting moves
        7: [BUBBLE_BEAM],
        13: [BITE],
        20: [HYDRO_PUMP]
    },
    "Bulbasaur": {
        1: [TACKLE, VINE_WHIP],  # Starting moves
        7: [RAZOR_LEAF],
        15: [SOLAR_BEAM]
    }
}


# All moves dictionary for save/load
ALL_MOVES = {
    "Thunderbolt": THUNDERBOLT,
    "Quick Attack": QUICK_ATTACK,
    "Thunder": THUNDER,
    "Iron Tail": IRON_TAIL,
    "Ember": EMBER,
    "Scratch": SCRATCH,
    "Flamethrower": FLAMETHROWER,
    "Metal Claw": METAL_CLAW,
    "Fire Blast": FIRE_BLAST,
    "Water Gun": WATER_GUN,
    "Tackle": TACKLE,
    "Bubble Beam": BUBBLE_BEAM,
    "Bite": BITE,
    "Hydro Pump": HYDRO_PUMP,
    "Vine Whip": VINE_WHIP,
    "Razor Leaf": RAZOR_LEAF,
    "Solar Beam": SOLAR_BEAM
}


def get_starting_moves(pokemon_name):
    """
    Get the starting moves for a Pokemon (level 1 moves).
    
    Args:
        pokemon_name (str): Name of the Pokemon
    
    Returns:
        list: List of Move objects
    """
    if pokemon_name not in LEARNSETS:
        return []
    
    learnset = LEARNSETS[pokemon_name]
    if 1 in learnset:
        return learnset[1][:4]  # Limit to 4 moves
    return []


def get_moves_at_level(pokemon_name, level):
    """
    Get moves that should be learned at a specific level.
    
    Args:
        pokemon_name (str): Name of the Pokemon
        level (int): Level to check
    
    Returns:
        list: List of Move objects to learn at this level
    """
    if pokemon_name not in LEARNSETS:
        return []
    
    learnset = LEARNSETS[pokemon_name]
    if level in learnset:
        return learnset[level]
    return []


# ============================================
# TEST SECTION
# ============================================
if __name__ == "__main__":
    print("=== Move Learnsets Test ===\n")
    
    for pokemon_name in ["Pikachu", "Charmander", "Squirtle", "Bulbasaur"]:
        print(f"{pokemon_name} Learnset:")
        
        if pokemon_name in LEARNSETS:
            learnset = LEARNSETS[pokemon_name]
            for level in sorted(set(learnset.keys())):
                moves = get_moves_at_level(pokemon_name, level)
                move_names = [m.name for m in moves]
                print(f"  Level {level}: {', '.join(move_names)}")
        
        print()
    
    print("=== Test Complete ===")
