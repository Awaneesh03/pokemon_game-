"""
FastAPI Pokemon Battle Game - WebSocket Multiplayer
Real-time multiplayer battle rooms with WebSockets
"""

import uuid
from typing import Dict, Optional, List
from enum import Enum
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pokemon import Pokemon
from battle import calculate_damage
from learnsets import get_starting_moves


class PlayerRole(Enum):
    PLAYER1 = "player1"
    PLAYER2 = "player2"


class BattleRoom:
    """Manages a multiplayer battle between two players"""
    
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.players: Dict[PlayerRole, Optional[dict]] = {
            PlayerRole.PLAYER1: None,
            PlayerRole.PLAYER2: None
        }
        self.pokemon: Dict[PlayerRole, Optional[Pokemon]] = {
            PlayerRole.PLAYER1: None,
            PlayerRole.PLAYER2: None
        }
        self.current_turn: Optional[PlayerRole] = None
        self.battle_started = False
        self.battle_ended = False
        self.winner: Optional[PlayerRole] = None
    
    def add_player(self, websocket, player_id: str) -> Optional[PlayerRole]:
        """Add a player to the room. Returns their role or None if room is full."""
        if self.players[PlayerRole.PLAYER1] is None:
            role = PlayerRole.PLAYER1
        elif self.players[PlayerRole.PLAYER2] is None:
            role = PlayerRole.PLAYER2
        else:
            return None  # Room is full
        
        self.players[role] = {
            "websocket": websocket,
            "player_id": player_id,
            "ready": False
        }
        return role
    
    def remove_player(self, role: PlayerRole):
        """Remove a player from the room"""
        self.players[role] = None
        self.pokemon[role] = None
    
    def is_full(self) -> bool:
        """Check if room has 2 players"""
        return all(p is not None for p in self.players.values())
    
    def is_empty(self) -> bool:
        """Check if room has no players"""
        return all(p is None for p in self.players.values())
    
    def set_pokemon(self, role: PlayerRole, pokemon: Pokemon):
        """Set a player's Pokemon"""
        self.pokemon[role] = pokemon
        if self.players[role]:
            self.players[role]["ready"] = True
    
    def both_ready(self) -> bool:
        """Check if both players have selected Pokemon"""
        return all(
            p is not None and p["ready"] 
            for p in self.players.values()
        )
    
    def start_battle(self):
        """Start the battle - determine first turn based on speed"""
        if not self.both_ready():
            return False
        
        p1_speed = self.pokemon[PlayerRole.PLAYER1].speed
        p2_speed = self.pokemon[PlayerRole.PLAYER2].speed
        
        # Faster Pokemon goes first
        if p1_speed >= p2_speed:
            self.current_turn = PlayerRole.PLAYER1
        else:
            self.current_turn = PlayerRole.PLAYER2
        
        self.battle_started = True
        return True
    
    def execute_move(self, role: PlayerRole, move_index: int) -> dict:
        """
        Execute a move and return battle results.
        
        Returns dict with:
        - success: bool
        - message: str
        - damage: int
        - critical: bool
        - effectiveness: float
        - battle_ended: bool
        - winner: Optional[str]
        """
        # Validate it's this player's turn
        if role != self.current_turn:
            return {
                "success": False,
                "message": "Not your turn!",
                "battle_ended": False
            }
        
        attacker = self.pokemon[role]
        defender_role = PlayerRole.PLAYER2 if role == PlayerRole.PLAYER1 else PlayerRole.PLAYER1
        defender = self.pokemon[defender_role]
        
        # Validate move index
        if move_index < 0 or move_index >= len(attacker.moves):
            return {
                "success": False,
                "message": "Invalid move index",
                "battle_ended": False
            }
        
        # Execute move
        move = attacker.moves[move_index]
        damage, effectiveness, is_critical = calculate_damage(attacker, defender, move)
        defender.take_damage(damage)
        
        result = {
            "success": True,
            "attacker": role.value,
            "move": move.name,
            "damage": damage,
            "critical": is_critical,
            "effectiveness": effectiveness,
            "message": f"{attacker.name} used {move.name}!",
            "battle_ended": False,
            "winner": None
        }
        
        # Check if defender fainted
        if defender.is_fainted():
            self.battle_ended = True
            self.winner = role
            result["battle_ended"] = True
            result["winner"] = role.value
        else:
            # Switch turns
            self.current_turn = defender_role
        
        return result
    
    def get_state(self) -> dict:
        """Get current battle state"""
        return {
            "room_id": self.room_id,
            "battle_started": self.battle_started,
            "battle_ended": self.battle_ended,
            "current_turn": self.current_turn.value if self.current_turn else None,
            "winner": self.winner.value if self.winner else None,
            "player1": {
                "connected": self.players[PlayerRole.PLAYER1] is not None,
                "ready": self.players[PlayerRole.PLAYER1]["ready"] if self.players[PlayerRole.PLAYER1] else False,
                "pokemon": self._pokemon_to_dict(PlayerRole.PLAYER1) if self.pokemon[PlayerRole.PLAYER1] else None
            },
            "player2": {
                "connected": self.players[PlayerRole.PLAYER2] is not None,
                "ready": self.players[PlayerRole.PLAYER2]["ready"] if self.players[PlayerRole.PLAYER2] else False,
                "pokemon": self._pokemon_to_dict(PlayerRole.PLAYER2) if self.pokemon[PlayerRole.PLAYER2] else None
            }
        }
    
    def _pokemon_to_dict(self, role: PlayerRole) -> dict:
        """Convert Pokemon to dict for JSON serialization"""
        pokemon = self.pokemon[role]
        if not pokemon:
            return None
        
        return {
            "name": pokemon.name,
            "type": pokemon.type,
            "level": pokemon.level,
            "current_hp": pokemon.current_hp,
            "max_hp": pokemon.max_hp,
            "attack": pokemon.attack,
            "defense": pokemon.defense,
            "speed": pokemon.speed,
            "moves": [
                {
                    "name": m.name,
                    "type": m.type,
                    "power": m.power,
                    "accuracy": m.accuracy
                }
                for m in pokemon.moves
            ]
        }


# Global room storage
battle_rooms: Dict[str, BattleRoom] = {}


def create_room() -> str:
    """Create a new battle room and return its ID"""
    room_id = str(uuid.uuid4())[:8]
    battle_rooms[room_id] = BattleRoom(room_id)
    return room_id


def get_room(room_id: str) -> Optional[BattleRoom]:
    """Get a battle room by ID"""
    return battle_rooms.get(room_id)


def cleanup_empty_rooms():
    """Remove empty rooms from storage"""
    empty_rooms = [rid for rid, room in battle_rooms.items() if room.is_empty()]
    for rid in empty_rooms:
        del battle_rooms[rid]
