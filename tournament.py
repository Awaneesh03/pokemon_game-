"""
Pokemon Battle Game - Tournament Mode
3 consecutive battles with increasing difficulty
"""

from pokemon import Pokemon
from move import Move
from battle import battle
from items import Inventory


def between_battle_menu(player_pokemon, inventory):
    """
    Menu shown between tournament battles.
    
    Args:
        player_pokemon (Pokemon): Player's Pokemon
        inventory (Inventory): Player's inventory
    """
    from save_load import save_game
    
    while True:
        print("\n" + "=" * 50)
        print("BETWEEN BATTLES")
        print("=" * 50)
        
        print("\nWhat would you like to do?")
        print("  1. View Pokemon Status")
        print("  2. Use Item")
        print("  3. Save Game")
        print("  4. Continue to Next Battle")
        
        try:
            choice = int(input("\nChoose option: "))
            
            if choice == 1:
                # View status
                print("\n--- Pokemon Status ---")
                player_pokemon.show_status()
                print(f"Level: {player_pokemon.level}")
                print(f"XP: {player_pokemon.xp}/{player_pokemon.level * 100}")
                print(f"Type: {player_pokemon.type}")
                print(f"ATK: {player_pokemon.attack}, DEF: {player_pokemon.defense}, SPD: {player_pokemon.speed}")
                
            elif choice == 2:
                # Use item
                available_items = inventory.get_available_items()
                
                if not available_items:
                    print("\nYou don't have any items!")
                else:
                    inventory.show_inventory()
                    
                    print("\nSelect an item:")
                    for i, item_key in enumerate(available_items, 1):
                        from items import ITEMS
                        print(f"  {i}. {ITEMS[item_key].name}")
                    print(f"  {len(available_items) + 1}. Cancel")
                    
                    try:
                        item_choice = int(input("\nChoose item: "))
                        if 1 <= item_choice <= len(available_items):
                            item_key = available_items[item_choice - 1]
                            success, message = inventory.use_item(item_key, player_pokemon)
                            print(f"\n{message}")
                        elif item_choice == len(available_items) + 1:
                            print("\nCancelled.")
                        else:
                            print("Invalid choice!")
                    except ValueError:
                        print("Please enter a valid number!")
                        
            elif choice == 3:
                # Save game
                save_game(player_pokemon, inventory)
                
            elif choice == 4:
                # Continue
                print("\nProceeding to next battle...")
                break
            else:
                print("Invalid choice! Choose 1, 2, 3, or 4")
                
        except ValueError:
            print("Please enter a valid number!")


def create_enemy(round_num):
    """
    Create an enemy Pokemon for the given round.
    
    Args:
        round_num (int): Round number (1-3)
    
    Returns:
        Pokemon: Enemy Pokemon with appropriate stats
    """
    if round_num == 1:
        # Round 1: Bulbasaur (Level 1-2)
        bulbasaur = Pokemon("Bulbasaur", "Grass", 45, 49, 49, 45)
        vine_whip = Move("Vine Whip", "Grass", 45, 100)
        tackle = Move("Tackle", "Normal", 40, 100)
        bulbasaur.moves = [vine_whip, tackle]
        return bulbasaur
        
    elif round_num == 2:
        # Round 2: Squirtle (Level 3)
        squirtle = Pokemon("Squirtle", "Water", 44, 48, 65, 43)
        squirtle.level = 3
        # Apply level-up stat boosts (2 levels worth)
        squirtle.max_hp += 20
        squirtle.current_hp = squirtle.max_hp
        squirtle.attack += 10
        squirtle.defense += 6
        squirtle.speed += 4
        
        water_gun = Move("Water Gun", "Water", 40, 100)
        tackle = Move("Tackle", "Normal", 40, 100)
        squirtle.moves = [water_gun, tackle]
        return squirtle
        
    elif round_num == 3:
        # Round 3: Charmander (Level 5)
        charmander = Pokemon("Charmander", "Fire", 39, 52, 43, 65)
        charmander.level = 5
        # Apply level-up stat boosts (4 levels worth)
        charmander.max_hp += 40
        charmander.current_hp = charmander.max_hp
        charmander.attack += 20
        charmander.defense += 12
        charmander.speed += 8
        
        ember = Move("Ember", "Fire", 40, 100)
        scratch = Move("Scratch", "Normal", 40, 100)
        metal_claw = Move("Metal Claw", "Normal", 50, 95)
        charmander.moves = [ember, scratch, metal_claw]
        return charmander


def tournament(player_pokemon, inventory):
    """
    Run a 3-round tournament.
    
    Args:
        player_pokemon (Pokemon): Player's Pokemon
        inventory (Inventory): Player's inventory
    
    Returns:
        bool: True if player won tournament, False if lost
    """
    print("=" * 50)
    print("🏆 POKEMON TOURNAMENT 🏆")
    print("=" * 50)
    print("\nDefeat 3 opponents to win the tournament!")
    print(f"Your Pokemon: {player_pokemon.name} (Level {player_pokemon.level})")
    print("\nPress Enter to begin...")
    input()
    
    for round_num in range(1, 4):
        print("\n" + "=" * 50)
        print(f"ROUND {round_num}/3")
        print("=" * 50)
        
        # Create enemy for this round
        enemy = create_enemy(round_num)
        
        print(f"\nOpponent: {enemy.name} (Level {enemy.level})")
        print("Press Enter to start battle...")
        input()
        
        # Battle
        battle(player_pokemon, enemy, inventory)
        
        # Check if player lost
        if player_pokemon.is_fainted():
            print("\n" + "=" * 50)
            print("💀 TOURNAMENT OVER 💀")
            print("=" * 50)
            print(f"\nYou were defeated in Round {round_num}!")
            print("Better luck next time!")
            return False
        
        # Player won this round
        print(f"\n✅ Round {round_num} Complete!")
        
        # Between battle menu (except after final round)
        if round_num < 3:
            between_battle_menu(player_pokemon, inventory)
    
    # Player won all 3 rounds!
    print("\n" + "=" * 50)
    print("🎉🏆 TOURNAMENT CHAMPION! 🏆🎉")
    print("=" * 50)
    print(f"\n{player_pokemon.name} has defeated all opponents!")
    print(f"Final Level: {player_pokemon.level}")
    print("Congratulations!")
    
    return True


def main():
    """
    Main function to start tournament mode.
    """
    from save_load import load_game, save_game
    
    print("=== Pokemon Tournament Mode ===\n")
    
    # Create all possible moves
    thunderbolt = Move("Thunderbolt", "Electric", 90, 100)
    quick_attack = Move("Quick Attack", "Normal", 40, 100)
    ember = Move("Ember", "Fire", 40, 100)
    scratch = Move("Scratch", "Normal", 40, 100)
    water_gun = Move("Water Gun", "Water", 40, 100)
    tackle = Move("Tackle", "Normal", 40, 100)
    
    all_moves = {
        "Thunderbolt": thunderbolt,
        "Quick Attack": quick_attack,
        "Ember": ember,
        "Scratch": scratch,
        "Water Gun": water_gun,
        "Tackle": tackle
    }
    
    # Check for save file
    print("Main Menu:")
    print("  1. New Game")
    print("  2. Load Game")
    
    while True:
        try:
            menu_choice = int(input("\nChoose option (1 or 2): "))
            if menu_choice in [1, 2]:
                break
            else:
                print("Invalid choice! Choose 1 or 2")
        except ValueError:
            print("Please enter a valid number!")
    
    player_pokemon = None
    inventory = None
    
    if menu_choice == 2:
        # Try to load game
        player_pokemon, inventory = load_game(all_moves)
        
        if not player_pokemon:
            print("\nNo save file found or load failed. Starting new game...")
            menu_choice = 1  # Fall back to new game
    
    if menu_choice == 1:
        # New game - let player choose their Pokemon
        print("\nChoose your Pokemon:")
        print("  1. Pikachu (Electric)")
        print("  2. Charmander (Fire)")
        print("  3. Squirtle (Water)")
        
        while True:
            try:
                choice = int(input("\nChoose Pokemon (1-3): "))
                if 1 <= choice <= 3:
                    break
                else:
                    print("Invalid choice! Choose 1, 2, or 3")
            except ValueError:
                print("Please enter a valid number!")
        
        # Create player's Pokemon
        if choice == 1:
            player_pokemon = Pokemon("Pikachu", "Electric", 35, 55, 40, 90)
            player_pokemon.moves = [thunderbolt, quick_attack]
        elif choice == 2:
            player_pokemon = Pokemon("Charmander", "Fire", 39, 52, 43, 65)
            player_pokemon.moves = [ember, scratch]
        else:
            player_pokemon = Pokemon("Squirtle", "Water", 44, 48, 65, 43)
            player_pokemon.moves = [water_gun, tackle]
        
        # Create inventory
        inventory = Inventory()
    
    # Start tournament
    tournament(player_pokemon, inventory)


if __name__ == "__main__":
    main()
