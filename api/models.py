"""
FastAPI Pokemon Battle Game - Pydantic Models
Request and response models for API endpoints
"""

from pydantic import BaseModel
from typing import List, Optional, Dict


# ============================================
# RESPONSE MODELS
# ============================================

class MoveInfo(BaseModel):
    """Information about a move"""
    name: str
    type: str
    power: int
    accuracy: int


class PokemonStats(BaseModel):
    """Pokemon base stats"""
    hp: int
    attack: int
    defense: int
    speed: int


class PokemonInfo(BaseModel):
    """Complete Pokemon information"""
    name: str
    type: str
    level: int
    xp: int
    current_hp: int
    max_hp: int
    attack: int
    defense: int
    speed: int
    moves: List[MoveInfo]


class InventoryInfo(BaseModel):
    """Player inventory information"""
    potion: int
    super_potion: int
    revive: int


class AvailablePokemon(BaseModel):
    """Available Pokemon for selection"""
    name: str
    type: str
    base_stats: PokemonStats
    starting_moves: List[str]


class PokemonListResponse(BaseModel):
    """Response for GET /pokemon"""
    pokemon: List[AvailablePokemon]


class SelectPokemonResponse(BaseModel):
    """Response for POST /select-pokemon"""
    message: str
    pokemon: PokemonInfo
    inventory: InventoryInfo


class BattleState(BaseModel):
    """Current battle state"""
    in_battle: bool
    turn: int
    player_pokemon: Optional[PokemonInfo]
    opponent_pokemon: Optional[PokemonInfo]


class TurnResult(BaseModel):
    """Result of a single turn action"""
    attacker: str
    move: str
    damage: int
    critical: bool
    effectiveness: float
    message: str


class BattleMoveResponse(BaseModel):
    """Response for POST /battle/move"""
    turn_results: List[TurnResult]
    player_pokemon: PokemonInfo
    opponent_pokemon: PokemonInfo
    battle_ended: bool
    winner: Optional[str]
    level_up_messages: Optional[List[str]] = None


class BattleItemResponse(BaseModel):
    """Response for POST /battle/item"""
    success: bool
    message: str
    turn_results: List[TurnResult]
    player_pokemon: PokemonInfo
    opponent_pokemon: PokemonInfo
    inventory: InventoryInfo
    battle_ended: bool
    winner: Optional[str]


class StartBattleResponse(BaseModel):
    """Response for POST /battle/start"""
    message: str
    player_pokemon: PokemonInfo
    opponent_pokemon: PokemonInfo
    turn: int


class SaveResponse(BaseModel):
    """Response for POST /save"""
    success: bool
    message: str


class LoadResponse(BaseModel):
    """Response for POST /load"""
    success: bool
    message: str
    pokemon: Optional[PokemonInfo]
    inventory: Optional[InventoryInfo]


# ============================================
# REQUEST MODELS
# ============================================

class SelectPokemonRequest(BaseModel):
    """Request to select a Pokemon"""
    pokemon_name: str


class StartBattleRequest(BaseModel):
    """Request to start a battle"""
    opponent_name: str


class UseMoveRequest(BaseModel):
    """Request to use a move"""
    move_index: int


class UseItemRequest(BaseModel):
    """Request to use an item"""
    item_key: str
