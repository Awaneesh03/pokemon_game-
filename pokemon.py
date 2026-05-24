"""
Pokemon Battle Game - Foundation
A simple Pokemon class for turn-based battles
"""


class Pokemon:
    """
    Represents a single Pokemon with stats and basic battle behaviors.
    
    Attributes:
        name (str): The Pokemon's name
        type (str): The Pokemon's type (e.g., 'Fire', 'Water', 'Grass')
        level (int): Current level (starts at 1)
        xp (int): Current experience points (starts at 0)
        max_hp (int): Maximum hit points
        current_hp (int): Current hit points (starts equal to max_hp)
        attack (int): Attack stat
        defense (int): Defense stat
        speed (int): Speed stat (determines turn order)
        moves (list): List of moves (empty for now)
    """
    
    def __init__(self, name, type, max_hp, attack, defense, speed):
        """
        Initialize a new Pokemon.
        
        Args:
            name (str): Pokemon's name
            type (str): Pokemon's type
            max_hp (int): Maximum HP
            attack (int): Attack stat
            defense (int): Defense stat
            speed (int): Speed stat
        """
        self.name = name
        self.type = type
        self.level = 1  # Start at level 1
        self.xp = 0  # Start with 0 XP
        self.max_hp = max_hp
        self.current_hp = max_hp  # Start at full health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = []  # Empty for now
    
    def is_fainted(self):
        """
        Check if the Pokemon has fainted.
        
        Returns:
            bool: True if current HP is 0 or less, False otherwise
        """
        return self.current_hp <= 0
    
    def take_damage(self, damage):
        """
        Reduce the Pokemon's HP by the damage amount.
        HP will never go below 0.
        
        Args:
            damage (int): Amount of damage to take
        """
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
    
    def show_status(self):
        """
        Display the Pokemon's current status.
        Shows name and HP in a clear format.
        """
        print(f"{self.name}: {self.current_hp}/{self.max_hp} HP")
    
    def show_moves(self):
        """
        Display all available moves for this Pokemon.
        Shows numbered list with move details.
        """
        if not self.moves:
            print("No moves available!")
            return
        
        print("Available moves:")
        for i, move in enumerate(self.moves, 1):
            print(f"  {i}. {move.name} ({move.type}) - Power: {move.power}, Accuracy: {move.accuracy}%")
    
    def learn_move(self, new_move, is_player=True):
        """
        Learn a new move. If Pokemon has 4 moves, ask player to replace one.
        
        Args:
            new_move (Move): The move to learn
            is_player (bool): True if player's Pokemon (prompts for choice), False for AI (auto-replace)
        
        Returns:
            bool: True if move was learned, False otherwise
        """
        # Check if already knows this move
        if any(move.name == new_move.name for move in self.moves):
            return False
        
        # If less than 4 moves, just add it
        if len(self.moves) < 4:
            self.moves.append(new_move)
            print(f"\n🎓 {self.name} learned {new_move.name}!")
            return True
        
        # Pokemon has 4 moves - need to replace one
        print(f"\n{self.name} wants to learn {new_move.name}!")
        print(f"But {self.name} already knows 4 moves.")
        
        if is_player:
            # Ask player which move to forget
            print("\nCurrent moves:")
            for i, move in enumerate(self.moves, 1):
                print(f"  {i}. {move.name} ({move.type}) - Power: {move.power}")
            print(f"  5. Don't learn {new_move.name}")
            
            while True:
                try:
                    choice = int(input("\nReplace which move? (1-5): "))
                    if 1 <= choice <= 5:
                        break
                    else:
                        print("Invalid choice! Choose 1-5")
                except ValueError:
                    print("Please enter a valid number!")
            
            if choice == 5:
                print(f"\n{self.name} did not learn {new_move.name}.")
                return False
            
            # Replace chosen move
            old_move = self.moves[choice - 1]
            self.moves[choice - 1] = new_move
            print(f"\n{self.name} forgot {old_move.name} and learned {new_move.name}!")
            return True
        else:
            # AI Pokemon - auto-replace weakest move
            weakest_idx = min(range(len(self.moves)), key=lambda i: self.moves[i].power)
            old_move = self.moves[weakest_idx]
            self.moves[weakest_idx] = new_move
            print(f"\n{self.name} forgot {old_move.name} and learned {new_move.name}!")
            return True
    
    def gain_xp(self, amount, is_player=True):
        """
        Gain experience points and level up if enough XP is earned.
        Supports multiple level-ups if enough XP is gained.
        
        Args:
            amount (int): Amount of XP to gain
            is_player (bool): True if player's Pokemon, False for AI
        """
        self.xp += amount
        print(f"\n{self.name} gained {amount} XP!")
        
        # Check for level-ups (support multiple level-ups)
        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            old_level = self.level
            self.level += 1
            
            # Increase stats
            self.max_hp += 10
            self.attack += 5
            self.defense += 3
            self.speed += 2
            
            # Restore HP to full
            self.current_hp = self.max_hp
            
            # Display level-up message
            print(f"\n🎊 {self.name} leveled up to Level {self.level}! 🎊")
            print(f"Stats increased: HP +10, ATK +5, DEF +3, SPD +2")
            print(f"HP fully restored!")
            print(f"New stats: HP {self.max_hp}, ATK {self.attack}, DEF {self.defense}, SPD {self.speed}")
            
            # Check for new moves to learn
            try:
                from learnsets import get_moves_at_level
                new_moves = get_moves_at_level(self.name, self.level)
                
                for new_move in new_moves:
                    self.learn_move(new_move, is_player)
            except ImportError:
                pass  # Learnsets not available


# ============================================
# TEST SECTION
# ============================================
if __name__ == "__main__":
    print("=== Pokemon Battle Game - Test ===\n")
    
    # Create a Pokemon
    pikachu = Pokemon(
        name="Pikachu",
        type="Electric",
        max_hp=35,
        attack=55,
        defense=40,
        speed=90
    )
    
    # Show initial status
    print("Initial status:")
    pikachu.show_status()
    print(f"Type: {pikachu.type}")
    print(f"Attack: {pikachu.attack}")
    print(f"Defense: {pikachu.defense}")
    print(f"Is fainted? {pikachu.is_fainted()}")
    
    # Take some damage
    print("\n--- Pikachu takes 15 damage! ---")
    pikachu.take_damage(15)
    pikachu.show_status()
    print(f"Is fainted? {pikachu.is_fainted()}")
    
    # Take more damage
    print("\n--- Pikachu takes 25 damage! ---")
    pikachu.take_damage(25)
    pikachu.show_status()
    print(f"Is fainted? {pikachu.is_fainted()}")
    
    # Try to go below 0 HP
    print("\n--- Pikachu takes 10 more damage! ---")
    pikachu.take_damage(10)
    pikachu.show_status()
    print(f"Is fainted? {pikachu.is_fainted()}")
    
    print("\n=== Test Complete ===")
