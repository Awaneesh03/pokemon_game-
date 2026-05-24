"""
FastAPI Pokemon Battle Game - Service Layer
Business logic wrapping existing game code
"""

import sys
import os
from typing import List, Tuple, Optional
from io import StringIO
import contextlib

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pokemon import Pokemon
from move import Move
from items import Inventory, ITEMS
from learnsets import get_starting_moves, ALL_MOVES
from battle import calculate_damage, choose_best_move, get_type_effectiveness
from save_load import save_game, load_game, pokemon_to_dict, dict_to_pokemon
from api.models import *


# Available Pokemon for selection
AVAILABLE_POKEMON = {
    "Pikachu": {"type": "Electric", "hp": 35, "attack": 55, "defense": 40, "speed": 90},
    "Charmander": {"type": "Fire", "hp": 39, "attack": 52, "defense": 43, "speed": 65},
    "Squirtle": {"type": "Water", "hp": 44, "attack": 48, "defense": 65, "speed": 43},
    "Bulbasaur": {"type": "Grass", "hp": 45, "attack": 49, "defense": 49, "speed": 45}
}


def get_available_pokemon() -> List[AvailablePokemon]:
    """Get list of available Pokemon for selection"""
    result = []
    for name, stats in AVAILABLE_POKEMON.items():
        starting_moves = get_starting_moves(name)
        result.append(AvailablePokemon(
            name=name,
            type=stats["type"],
            base_stats=PokemonStats(
                hp=stats["hp"],
                attack=stats["attack"],
                defense=stats["defense"],
                speed=stats["speed"]
            ),
            starting_moves=[m.name for m in starting_moves]
        ))
    return result


def create_pokemon(name: str) -> Optional[Pokemon]:
    """Create a Pokemon instance"""
    if name not in AVAILABLE_POKEMON:
        return None
    
    stats = AVAILABLE_POKEMON[name]
    pokemon = Pokemon(
        name=name,
        type=stats["type"],
        max_hp=stats["hp"],
        attack=stats["attack"],
        defense=stats["defense"],
        speed=stats["speed"]
    )
    
    # Set starting moves
    pokemon.moves = get_starting_moves(name)
    
    return pokemon


def pokemon_to_info(pokemon: Pokemon) -> PokemonInfo:
    """Convert Pokemon object to PokemonInfo model"""
    return PokemonInfo(
        name=pokemon.name,
        type=pokemon.type,
        level=pokemon.level,
        xp=pokemon.xp,
        current_hp=pokemon.current_hp,
        max_hp=pokemon.max_hp,
        attack=pokemon.attack,
        defense=pokemon.defense,
        speed=pokemon.speed,
        moves=[MoveInfo(
            name=m.name,
            type=m.type,
            power=m.power,
            accuracy=m.accuracy
        ) for m in pokemon.moves]
    )


def inventory_to_info(inventory: Inventory) -> InventoryInfo:
    """Convert Inventory object to InventoryInfo model"""
    return InventoryInfo(
        potion=inventory.items.get('potion', 0),
        super_potion=inventory.items.get('super_potion', 0),
        revive=inventory.items.get('revive', 0)
    )


@contextlib.contextmanager
def capture_output():
    """Capture stdout to suppress print statements"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout = old_stdout


def execute_battle_turn(player_pokemon: Pokemon, opponent_pokemon: Pokemon, 
                       player_move_index: int) -> Tuple[List[TurnResult], bool, Optional[str], List[str]]:
    """
    Execute a battle turn with player move and opponent AI response.
    
    Returns:
        (turn_results, battle_ended, winner, level_up_messages)
    """
    results = []
    battle_ended = False
    winner = None
    level_up_messages = []
    
    # Determine turn order based on speed
    if player_pokemon.speed >= opponent_pokemon.speed:
        first_attacker = player_pokemon
        first_defender = opponent_pokemon
        second_attacker = opponent_pokemon
        second_defender = player_pokemon
        first_is_player = True
    else:
        first_attacker = opponent_pokemon
        first_defender = player_pokemon
        second_attacker = player_pokemon
        second_defender = opponent_pokemon
        first_is_player = False
    
    # First attacker's turn
    if first_is_player:
        move = player_pokemon.moves[player_move_index]
    else:
        move = choose_best_move(opponent_pokemon, player_pokemon)
    
    damage, effectiveness, is_critical = calculate_damage(first_attacker, first_defender, move)
    first_defender.take_damage(damage)
    
    results.append(TurnResult(
        attacker=first_attacker.name,
        move=move.name,
        damage=damage,
        critical=is_critical,
        effectiveness=effectiveness,
        message=f"{first_attacker.name} used {move.name}!"
    ))
    
    # Check if defender fainted
    if first_defender.is_fainted():
        battle_ended = True
        winner = first_attacker.name
        
        # Award XP with captured output
        with capture_output() as output:
            first_attacker.gain_xp(50, is_player=first_is_player)
            level_up_output = output.getvalue()
            if "leveled up" in level_up_output:
                level_up_messages = [line.strip() for line in level_up_output.split('\n') if line.strip()]
        
        return results, battle_ended, winner, level_up_messages
    
    # Second attacker's turn
    if not first_is_player:
        move = player_pokemon.moves[player_move_index]
    else:
        move = choose_best_move(opponent_pokemon, player_pokemon)
    
    damage, effectiveness, is_critical = calculate_damage(second_attacker, second_defender, move)
    second_defender.take_damage(damage)
    
    results.append(TurnResult(
        attacker=second_attacker.name,
        move=move.name,
        damage=damage,
        critical=is_critical,
        effectiveness=effectiveness,
        message=f"{second_attacker.name} used {move.name}!"
    ))
    
    # Check if defender fainted
    if second_defender.is_fainted():
        battle_ended = True
        winner = second_attacker.name
        
        # Award XP with captured output
        with capture_output() as output:
            second_attacker.gain_xp(50, is_player=not first_is_player)
            level_up_output = output.getvalue()
            if "leveled up" in level_up_output:
                level_up_messages = [line.strip() for line in level_up_output.split('\n') if line.strip()]
    
    return results, battle_ended, winner, level_up_messages


def execute_item_turn(player_pokemon: Pokemon, opponent_pokemon: Pokemon,
                     inventory: Inventory, item_key: str) -> Tuple[bool, str, List[TurnResult], bool, Optional[str]]:
    """
    Execute a turn where player uses an item, then opponent attacks.
    
    Returns:
        (success, message, turn_results, battle_ended, winner)
    """
    # Use item with captured output
    with capture_output():
        success, message = inventory.use_item(item_key, player_pokemon)
    
    if not success:
        return False, message, [], False, None
    
    # Opponent's turn
    results = []
    battle_ended = False
    winner = None
    
    move = choose_best_move(opponent_pokemon, player_pokemon)
    damage, effectiveness, is_critical = calculate_damage(opponent_pokemon, player_pokemon, move)
    player_pokemon.take_damage(damage)
    
    results.append(TurnResult(
        attacker=opponent_pokemon.name,
        move=move.name,
        damage=damage,
        critical=is_critical,
        effectiveness=effectiveness,
        message=f"{opponent_pokemon.name} used {move.name}!"
    ))
    
    # Check if player fainted
    if player_pokemon.is_fainted():
        battle_ended = True
        winner = opponent_pokemon.name
        
        # Award XP to opponent
        with capture_output():
            opponent_pokemon.gain_xp(50, is_player=False)
    
    return success, message, results, battle_ended, winner
