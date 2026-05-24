"""
Pokemon Battle Game - Save/Load System
Save and load game progress using JSON
"""

import json
import os
from pokemon import Pokemon
from move import Move
from items import Inventory, ITEMS


SAVE_FILE = "save_game.json"


def pokemon_to_dict(pokemon):
    """
    Convert a Pokemon object to a dictionary for JSON serialization.
    
    Args:
        pokemon (Pokemon): Pokemon to serialize
    
    Returns:
        dict: Serializable dictionary
    """
    return {
        'name': pokemon.name,
        'type': pokemon.type,
        'level': pokemon.level,
        'xp': pokemon.xp,
        'max_hp': pokemon.max_hp,
        'current_hp': pokemon.current_hp,
        'attack': pokemon.attack,
        'defense': pokemon.defense,
        'speed': pokemon.speed,
        'moves': [move.name for move in pokemon.moves]  # Store move names only
    }


def dict_to_pokemon(data, all_moves):
    """
    Reconstruct a Pokemon object from a dictionary.
    
    Args:
        data (dict): Pokemon data dictionary
        all_moves (dict): Dictionary of move name -> Move object
    
    Returns:
        Pokemon: Reconstructed Pokemon
    """
    # Create Pokemon with base stats
    pokemon = Pokemon(
        name=data['name'],
        type=data['type'],
        max_hp=data['max_hp'],
        attack=data['attack'],
        defense=data['defense'],
        speed=data['speed']
    )
    
    # Restore level and XP
    pokemon.level = data['level']
    pokemon.xp = data['xp']
    
    # Restore current HP
    pokemon.current_hp = data['current_hp']
    
    # Restore moves
    pokemon.moves = [all_moves[move_name] for move_name in data['moves'] if move_name in all_moves]
    
    return pokemon


def inventory_to_dict(inventory):
    """
    Convert an Inventory object to a dictionary.
    
    Args:
        inventory (Inventory): Inventory to serialize
    
    Returns:
        dict: Serializable dictionary
    """
    return inventory.items.copy()


def dict_to_inventory(data):
    """
    Reconstruct an Inventory object from a dictionary.
    
    Args:
        data (dict): Inventory data dictionary
    
    Returns:
        Inventory: Reconstructed Inventory
    """
    inventory = Inventory()
    inventory.items = data.copy()
    return inventory


def save_game(pokemon, inventory):
    """
    Save the game state to a JSON file.
    
    Args:
        pokemon (Pokemon): Player's Pokemon
        inventory (Inventory): Player's inventory
    
    Returns:
        bool: True if save succeeded, False otherwise
    """
    try:
        save_data = {
            'pokemon': pokemon_to_dict(pokemon),
            'inventory': inventory_to_dict(inventory)
        }
        
        with open(SAVE_FILE, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"\n✅ Game saved successfully to {SAVE_FILE}!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error saving game: {e}")
        return False


def load_game(all_moves):
    """
    Load the game state from a JSON file.
    
    Args:
        all_moves (dict): Dictionary of move name -> Move object
    
    Returns:
        tuple: (Pokemon, Inventory) or (None, None) if load failed
    """
    if not os.path.exists(SAVE_FILE):
        print(f"\n⚠️  No save file found ({SAVE_FILE})")
        return None, None
    
    try:
        with open(SAVE_FILE, 'r') as f:
            save_data = json.load(f)
        
        pokemon = dict_to_pokemon(save_data['pokemon'], all_moves)
        inventory = dict_to_inventory(save_data['inventory'])
        
        print(f"\n✅ Game loaded successfully!")
        print(f"Loaded: {pokemon.name} (Level {pokemon.level})")
        
        return pokemon, inventory
        
    except Exception as e:
        print(f"\n❌ Error loading game: {e}")
        return None, None


def delete_save():
    """
    Delete the save file.
    
    Returns:
        bool: True if deleted, False if file didn't exist
    """
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print(f"\n🗑️  Save file deleted.")
        return True
    return False


# ============================================
# TEST SECTION
# ============================================
if __name__ == "__main__":
    print("=== Save/Load System Test ===\n")
    
    # Create test moves
    thunderbolt = Move("Thunderbolt", "Electric", 90, 100)
    quick_attack = Move("Quick Attack", "Normal", 40, 100)
    
    all_moves = {
        "Thunderbolt": thunderbolt,
        "Quick Attack": quick_attack
    }
    
    # Create test Pokemon
    pikachu = Pokemon("Pikachu", "Electric", 35, 55, 40, 90)
    pikachu.moves = [thunderbolt, quick_attack]
    pikachu.level = 3
    pikachu.xp = 50
    pikachu.current_hp = 25
    
    # Create test inventory
    inventory = Inventory()
    inventory.items['potion'] = 5
    inventory.items['super_potion'] = 1
    
    print("Original Pokemon:")
    print(f"  {pikachu.name} - Level {pikachu.level}, XP: {pikachu.xp}")
    print(f"  HP: {pikachu.current_hp}/{pikachu.max_hp}")
    print(f"  Moves: {[m.name for m in pikachu.moves]}")
    
    print("\nOriginal Inventory:")
    inventory.show_inventory()
    
    # Test save
    print("\n--- Testing Save ---")
    save_game(pikachu, inventory)
    
    # Test load
    print("\n--- Testing Load ---")
    loaded_pokemon, loaded_inventory = load_game(all_moves)
    
    if loaded_pokemon and loaded_inventory:
        print("\nLoaded Pokemon:")
        print(f"  {loaded_pokemon.name} - Level {loaded_pokemon.level}, XP: {loaded_pokemon.xp}")
        print(f"  HP: {loaded_pokemon.current_hp}/{loaded_pokemon.max_hp}")
        print(f"  Moves: {[m.name for m in loaded_pokemon.moves]}")
        
        print("\nLoaded Inventory:")
        loaded_inventory.show_inventory()
    
    # Clean up
    print("\n--- Cleaning up test file ---")
    delete_save()
    
    print("\n=== Test Complete ===")
