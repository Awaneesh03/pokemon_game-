"""
FastAPI Pokemon Battle Game - State Management
In-memory game state for the API
"""

from typing import Optional
import sys
import os

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pokemon import Pokemon
from items import Inventory


class GameState:
    """Global game state (in-memory)"""
    
    def __init__(self):
        self.player_pokemon: Optional[Pokemon] = None
        self.opponent_pokemon: Optional[Pokemon] = None
        self.inventory: Optional[Inventory] = None
        self.in_battle: bool = False
        self.turn: int = 0
    
    def reset(self):
        """Reset game state"""
        self.player_pokemon = None
        self.opponent_pokemon = None
        self.inventory = None
        self.in_battle = False
        self.turn = 0
    
    def start_battle(self, opponent: Pokemon):
        """Start a new battle"""
        self.opponent_pokemon = opponent
        self.in_battle = True
        self.turn = 1
    
    def end_battle(self):
        """End the current battle"""
        self.in_battle = False
        self.opponent_pokemon = None


# Global game state instance
game_state = GameState()
