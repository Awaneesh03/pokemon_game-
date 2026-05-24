"""
Pokemon Battle Game - Items System
Item definitions and inventory management
"""


class Item:
    """
    Represents a usable item in battle.
    
    Attributes:
        name (str): Item name
        description (str): What the item does
        effect_type (str): Type of effect ('heal', 'revive')
        effect_value (int): Amount of HP restored or percentage
    """
    
    def __init__(self, name, description, effect_type, effect_value):
        """
        Initialize an item.
        
        Args:
            name (str): Item name
            description (str): Item description
            effect_type (str): 'heal' or 'revive'
            effect_value (int): HP amount or percentage
        """
        self.name = name
        self.description = description
        self.effect_type = effect_type
        self.effect_value = effect_value
    
    def use(self, pokemon):
        """
        Use the item on a Pokemon.
        
        Args:
            pokemon (Pokemon): The Pokemon to use the item on
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if self.effect_type == 'heal':
            # Cannot heal a fainted Pokemon with regular healing items
            if pokemon.is_fainted():
                return False, f"{pokemon.name} has fainted! Use a Revive instead."
            
            # Calculate healing
            old_hp = pokemon.current_hp
            pokemon.current_hp = min(pokemon.current_hp + self.effect_value, pokemon.max_hp)
            healed = pokemon.current_hp - old_hp
            
            if healed == 0:
                return False, f"{pokemon.name} is already at full HP!"
            
            return True, f"{pokemon.name} restored {healed} HP!"
        
        elif self.effect_type == 'revive':
            # Can only revive fainted Pokemon
            if not pokemon.is_fainted():
                return False, f"{pokemon.name} hasn't fainted!"
            
            # Revive with percentage of max HP
            pokemon.current_hp = int(pokemon.max_hp * (self.effect_value / 100))
            
            return True, f"{pokemon.name} was revived with {pokemon.current_hp} HP!"
        
        return False, "Unknown item effect!"


# Define available items
ITEMS = {
    'potion': Item(
        name="Potion",
        description="Heals 30 HP",
        effect_type='heal',
        effect_value=30
    ),
    'super_potion': Item(
        name="Super Potion",
        description="Heals 60 HP",
        effect_type='heal',
        effect_value=60
    ),
    'revive': Item(
        name="Revive",
        description="Revives a fainted Pokemon with 50% HP",
        effect_type='revive',
        effect_value=50
    )
}


class Inventory:
    """
    Manages player's item inventory.
    """
    
    def __init__(self):
        """Initialize inventory with starting items."""
        self.items = {
            'potion': 3,
            'super_potion': 2,
            'revive': 1
        }
    
    def has_item(self, item_key):
        """
        Check if player has at least one of the item.
        
        Args:
            item_key (str): Item key
        
        Returns:
            bool: True if item count > 0
        """
        return self.items.get(item_key, 0) > 0
    
    def use_item(self, item_key, pokemon):
        """
        Use an item from inventory on a Pokemon.
        
        Args:
            item_key (str): Item key
            pokemon (Pokemon): Pokemon to use item on
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.has_item(item_key):
            return False, f"You don't have any {ITEMS[item_key].name}s!"
        
        item = ITEMS[item_key]
        success, message = item.use(pokemon)
        
        if success:
            self.items[item_key] -= 1
        
        return success, message
    
    def show_inventory(self):
        """Display current inventory."""
        print("\n--- Items ---")
        has_items = False
        for key, count in self.items.items():
            if count > 0:
                item = ITEMS[key]
                print(f"  {item.name} x{count} - {item.description}")
                has_items = True
        
        if not has_items:
            print("  No items available!")
    
    def get_available_items(self):
        """
        Get list of available item keys.
        
        Returns:
            list: List of item keys with count > 0
        """
        return [key for key, count in self.items.items() if count > 0]


# ============================================
# TEST SECTION
# ============================================
if __name__ == "__main__":
    from pokemon import Pokemon
    
    print("=== Items System Test ===\n")
    
    # Create test Pokemon
    pikachu = Pokemon("Pikachu", "Electric", 35, 55, 40, 90)
    
    # Create inventory
    inventory = Inventory()
    
    print("Initial state:")
    pikachu.show_status()
    inventory.show_inventory()
    
    # Test 1: Damage Pokemon
    print("\n--- Test 1: Take damage ---")
    pikachu.take_damage(20)
    pikachu.show_status()
    
    # Test 2: Use Potion
    print("\n--- Test 2: Use Potion ---")
    success, message = inventory.use_item('potion', pikachu)
    print(message)
    pikachu.show_status()
    inventory.show_inventory()
    
    # Test 3: Use Super Potion
    print("\n--- Test 3: Use Super Potion ---")
    success, message = inventory.use_item('super_potion', pikachu)
    print(message)
    pikachu.show_status()
    
    # Test 4: Faint Pokemon and revive
    print("\n--- Test 4: Faint and Revive ---")
    pikachu.take_damage(100)
    pikachu.show_status()
    print(f"Is fainted? {pikachu.is_fainted()}")
    
    success, message = inventory.use_item('revive', pikachu)
    print(message)
    pikachu.show_status()
    print(f"Is fainted? {pikachu.is_fainted()}")
    
    print("\n=== Test Complete ===")
