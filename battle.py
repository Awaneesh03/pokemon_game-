"""
Pokemon Battle Game - Battle System
Turn-based battle system with simple damage calculation
"""

import random
from pokemon import Pokemon
from move import Move


# Type effectiveness chart
# Format: {attacking_type: {defending_type: multiplier}}
TYPE_EFFECTIVENESS = {
    "Fire": {
        "Grass": 2.0,  # Super effective
        "Water": 0.5,  # Not very effective
    },
    "Grass": {
        "Water": 2.0,  # Super effective
        "Fire": 0.5,   # Not very effective
    },
    "Water": {
        "Fire": 2.0,   # Super effective
        "Grass": 0.5,  # Not very effective
    },
    "Electric": {
        "Water": 2.0,  # Super effective
    },
}


def get_type_effectiveness(move_type, defender_type):
    """
    Get the type effectiveness multiplier.
    
    Args:
        move_type (str): The type of the move being used
        defender_type (str): The type of the defending Pokemon
    
    Returns:
        float: Damage multiplier (2.0 = super effective, 0.5 = not very effective, 1.0 = neutral)
    """
    if move_type in TYPE_EFFECTIVENESS:
        if defender_type in TYPE_EFFECTIVENESS[move_type]:
            return TYPE_EFFECTIVENESS[move_type][defender_type]
    return 1.0  # Neutral effectiveness


def choose_best_move(attacker, defender):
    """
    Choose the best move for the AI opponent based on type effectiveness and damage.
    
    AI Strategy (in priority order):
    1. Prefer super-effective moves (2.0x damage)
    2. Among those, choose highest expected damage
    3. If no super-effective moves, choose highest damage move
    4. Add 15% randomness to avoid perfect predictability
    
    Args:
        attacker (Pokemon): The attacking Pokemon
        defender (Pokemon): The defending Pokemon
    
    Returns:
        Move: The chosen move
    """
    if not attacker.moves:
        return None
    
    # 15% chance to choose randomly for unpredictability
    if random.random() < 0.15:
        return random.choice(attacker.moves)
    
    # Evaluate all moves
    move_scores = []
    for move in attacker.moves:
        # Calculate expected damage (without critical hit)
        base_damage = move.power + attacker.attack - defender.defense
        base_damage = max(base_damage, 1)
        
        # Get type effectiveness
        effectiveness = get_type_effectiveness(move.type, defender.type)
        
        # Calculate expected damage with type effectiveness
        expected_damage = base_damage * effectiveness
        
        move_scores.append({
            'move': move,
            'damage': expected_damage,
            'effectiveness': effectiveness
        })
    
    # Sort by effectiveness (descending), then by damage (descending)
    move_scores.sort(key=lambda x: (x['effectiveness'], x['damage']), reverse=True)
    
    # Return the best move
    return move_scores[0]['move']


def calculate_damage(attacker, defender, move):
    """
    Calculate damage using a simple formula with type effectiveness and critical hits.
    
    Args:
        attacker (Pokemon): The attacking Pokemon
        defender (Pokemon): The defending Pokemon
        move (Move): The move being used
    
    Returns:
        tuple: (damage amount, effectiveness multiplier, is_critical)
    """
    # Base damage calculation
    damage = move.power + attacker.attack - defender.defense
    damage = max(damage, 1)  # Minimum 1 damage
    
    # Apply type effectiveness
    effectiveness = get_type_effectiveness(move.type, defender.type)
    damage = int(damage * effectiveness)
    damage = max(damage, 1)  # Ensure at least 1 damage
    
    # Critical hit check (10% chance)
    is_critical = random.random() < 0.10
    if is_critical:
        damage = int(damage * 1.5)
    
    return damage, effectiveness, is_critical


def player_turn(player_pokemon, opponent_pokemon, inventory=None):
    """
    Handle the player's turn.
    
    Args:
        player_pokemon (Pokemon): Player's Pokemon
        opponent_pokemon (Pokemon): Opponent's Pokemon
        inventory (Inventory): Player's item inventory (optional)
    
    Returns:
        bool: True if attack was successful, False otherwise
    """
    print("\n--- Your Turn ---")
    
    # If inventory is provided, give option to use items
    if inventory:
        print("\nWhat will you do?")
        print("  1. Attack")
        print("  2. Use Item")
        
        while True:
            try:
                action = int(input("\nChoose action (1 or 2): "))
                if action in [1, 2]:
                    break
                else:
                    print("Invalid choice! Choose 1 or 2")
            except ValueError:
                print("Please enter a valid number!")
        
        # Handle item usage
        if action == 2:
            available_items = inventory.get_available_items()
            
            if not available_items:
                print("\nYou don't have any items!")
                print("You must attack instead.")
            else:
                inventory.show_inventory()
                
                # Show item options
                print("\nSelect an item:")
                for i, item_key in enumerate(available_items, 1):
                    from items import ITEMS
                    print(f"  {i}. {ITEMS[item_key].name}")
                print(f"  {len(available_items) + 1}. Cancel")
                
                while True:
                    try:
                        choice = int(input("\nChoose item: "))
                        if 1 <= choice <= len(available_items) + 1:
                            break
                        else:
                            print(f"Invalid choice! Choose between 1 and {len(available_items) + 1}")
                    except ValueError:
                        print("Please enter a valid number!")
                
                # Cancel and attack instead
                if choice == len(available_items) + 1:
                    print("\nCancelled! Choosing attack instead.")
                else:
                    item_key = available_items[choice - 1]
                    success, message = inventory.use_item(item_key, player_pokemon)
                    print(f"\n{message}")
                    
                    if success:
                        return True  # Item used successfully, turn ends
                    else:
                        print("Item usage failed! You must attack instead.")
    
    # Attack (either chosen or forced)
    player_pokemon.show_moves()
    
    # Get player's move choice
    while True:
        try:
            choice = int(input("\nChoose a move (enter number): "))
            if 1 <= choice <= len(player_pokemon.moves):
                chosen_move = player_pokemon.moves[choice - 1]
                break
            else:
                print(f"Invalid choice! Choose between 1 and {len(player_pokemon.moves)}")
        except ValueError:
            print("Please enter a valid number!")
    
    # Calculate and apply damage
    damage, effectiveness, is_critical = calculate_damage(player_pokemon, opponent_pokemon, chosen_move)
    
    print(f"\n{player_pokemon.name} used {chosen_move.name}!")
    
    # Show critical hit message
    if is_critical:
        print("A critical hit!")
    
    # Show effectiveness message
    if effectiveness > 1.0:
        print("It's super effective!")
    elif effectiveness < 1.0:
        print("It's not very effective...")
    
    print(f"It dealt {damage} damage!")
    
    opponent_pokemon.take_damage(damage)
    
    return True


def opponent_turn(opponent_pokemon, player_pokemon):
    """
    Handle the opponent's turn (AI chooses best move strategically).
    
    Args:
        opponent_pokemon (Pokemon): Opponent's Pokemon
        player_pokemon (Pokemon): Player's Pokemon
    
    Returns:
        bool: True if attack was successful, False otherwise
    """
    print("\n--- Opponent's Turn ---")
    
    # AI chooses best move strategically
    chosen_move = choose_best_move(opponent_pokemon, player_pokemon)
    
    # Calculate and apply damage
    damage, effectiveness, is_critical = calculate_damage(opponent_pokemon, player_pokemon, chosen_move)
    
    print(f"{opponent_pokemon.name} used {chosen_move.name}!")
    
    # Show critical hit message
    if is_critical:
        print("A critical hit!")
    
    # Show effectiveness message
    if effectiveness > 1.0:
        print("It's super effective!")
    elif effectiveness < 1.0:
        print("It's not very effective...")
    
    print(f"It dealt {damage} damage!")
    
    player_pokemon.take_damage(damage)
    
    return True


def execute_turn(attacker, defender, is_player, inventory=None):
    """
    Execute a single turn for either player or opponent.
    
    Args:
        attacker (Pokemon): The attacking Pokemon
        defender (Pokemon): The defending Pokemon
        is_player (bool): True if attacker is player's Pokemon
        inventory (Inventory): Player's item inventory (optional)
    
    Returns:
        bool: True if attack was successful
    """
    if is_player:
        return player_turn(attacker, defender, inventory)
    else:
        return opponent_turn(attacker, defender)


def battle(player_pokemon, opponent_pokemon, inventory=None):
    """
    Main battle loop between two Pokemon with speed-based turn order.
    
    Args:
        player_pokemon (Pokemon): Player's Pokemon
        opponent_pokemon (Pokemon): Opponent's Pokemon
        inventory (Inventory): Player's item inventory (optional)
    """
    print("=" * 50)
    print("POKEMON BATTLE START!")
    print("=" * 50)
    
    print(f"\n{player_pokemon.name} vs {opponent_pokemon.name}!")
    
    # Battle loop
    turn_count = 0
    while True:
        turn_count += 1
        print(f"\n{'=' * 50}")
        print(f"TURN {turn_count}")
        print("=" * 50)
        
        # Show status of both Pokemon
        print("\n--- Current Status ---")
        player_pokemon.show_status()
        opponent_pokemon.show_status()
        
        # Determine turn order based on speed
        if player_pokemon.speed >= opponent_pokemon.speed:
            # Player is faster (or equal speed, player goes first)
            first_attacker = player_pokemon
            first_defender = opponent_pokemon
            first_is_player = True
            second_attacker = opponent_pokemon
            second_defender = player_pokemon
            second_is_player = False
            
            if player_pokemon.speed > opponent_pokemon.speed:
                print(f"\n{player_pokemon.name} is faster!")
        else:
            # Opponent is faster
            first_attacker = opponent_pokemon
            first_defender = player_pokemon
            first_is_player = False
            second_attacker = player_pokemon
            second_defender = opponent_pokemon
            second_is_player = True
            
            print(f"\n{opponent_pokemon.name} is faster!")
        
        # First attacker's turn
        execute_turn(first_attacker, first_defender, first_is_player, inventory if first_is_player else None)
        
        # Check if defender fainted
        if first_defender.is_fainted():
            print(f"\n{first_defender.name} fainted!")
            if first_is_player:
                print(f"\n🎉 {player_pokemon.name} wins! 🎉")
                player_pokemon.gain_xp(50, is_player=True)  # Player Pokemon
            else:
                print(f"\n💀 {opponent_pokemon.name} wins! 💀")
                opponent_pokemon.gain_xp(50, is_player=False)  # AI Pokemon
            break
        
        # Second attacker's turn
        execute_turn(second_attacker, second_defender, second_is_player, inventory if second_is_player else None)
        
        # Check if defender fainted
        if second_defender.is_fainted():
            print(f"\n{second_defender.name} fainted!")
            if second_is_player:
                print(f"\n🎉 {player_pokemon.name} wins! 🎉")
                player_pokemon.gain_xp(50, is_player=True)  # Player Pokemon
            else:
                print(f"\n💀 {opponent_pokemon.name} wins! 💀")
                opponent_pokemon.gain_xp(50, is_player=False)  # AI Pokemon
            break
    
    print("\n" + "=" * 50)
    print("BATTLE END!")
    print("=" * 50)


def main():
    """
    Main function to set up and start a battle.
    """
    from items import Inventory
    
    # Create moves
    thunderbolt = Move("Thunderbolt", "Electric", 90, 100)
    quick_attack = Move("Quick Attack", "Normal", 40, 100)
    ember = Move("Ember", "Fire", 40, 100)
    scratch = Move("Scratch", "Normal", 40, 100)
    
    # Create Pokemon with speed stats
    # Pikachu is faster (speed 90 vs 65)
    pikachu = Pokemon("Pikachu", "Electric", 35, 55, 40, 90)
    pikachu.moves = [thunderbolt, quick_attack]
    
    charmander = Pokemon("Charmander", "Fire", 39, 52, 43, 65)
    charmander.moves = [ember, scratch]
    
    # Create inventory
    inventory = Inventory()
    
    # Start battle with inventory
    battle(pikachu, charmander, inventory)


if __name__ == "__main__":
    main()
