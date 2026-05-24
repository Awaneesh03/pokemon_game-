"""
FastAPI Pokemon Battle Game - Complete Main Application
REST API endpoints and WebSocket multiplayer
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models import *
from api.state import game_state
from api.services import *
from api.multiplayer import (
    battle_rooms, create_room, get_room, cleanup_empty_rooms,
    PlayerRole
)
from items import Inventory
from save_load import save_game, load_game
from learnsets import ALL_MOVES


# Create FastAPI app
app = FastAPI(
    title="Pokemon Battle Game API",
    description="REST API and WebSocket multiplayer for Pokemon battle game",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# REST API ENDPOINTS
# ============================================

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Pokemon Battle Game API with Multiplayer",
        "docs": "/docs",
        "endpoints": [
            "GET /pokemon",
            "POST /select-pokemon",
            "POST /battle/start",
            "POST /battle/move",
            "POST /battle/item",
            "GET /battle/status",
            "POST /save",
            "POST /load",
            "POST /multiplayer/create-room",
            "GET /multiplayer/rooms",
            "WS /ws/battle/{room_id}"
        ]
    }


@app.get("/pokemon", response_model=PokemonListResponse)
def list_pokemon():
    """Get list of available Pokemon"""
    pokemon_list = get_available_pokemon()
    return PokemonListResponse(pokemon=pokemon_list)


@app.post("/select-pokemon", response_model=SelectPokemonResponse)
def select_pokemon(request: SelectPokemonRequest):
    """Select a Pokemon to start the game"""
    pokemon = create_pokemon(request.pokemon_name)
    if not pokemon:
        raise HTTPException(status_code=400, detail=f"Invalid Pokemon: {request.pokemon_name}")
    
    game_state.player_pokemon = pokemon
    game_state.inventory = Inventory()
    game_state.in_battle = False
    
    return SelectPokemonResponse(
        message=f"Selected {pokemon.name}",
        pokemon=pokemon_to_info(pokemon),
        inventory=inventory_to_info(game_state.inventory)
    )


@app.post("/battle/start", response_model=StartBattleResponse)
def start_battle(request: StartBattleRequest):
    """Start a battle against an opponent"""
    if not game_state.player_pokemon:
        raise HTTPException(status_code=400, detail="No Pokemon selected")
    
    opponent = create_pokemon(request.opponent_name)
    if not opponent:
        raise HTTPException(status_code=400, detail=f"Invalid opponent: {request.opponent_name}")
    
    game_state.start_battle(opponent)
    
    return StartBattleResponse(
        message=f"Battle started against {opponent.name}",
        player_pokemon=pokemon_to_info(game_state.player_pokemon),
        opponent_pokemon=pokemon_to_info(opponent),
        turn=game_state.turn
    )


@app.post("/battle/move", response_model=BattleMoveResponse)
def use_move(request: UseMoveRequest):
    """Use a move in battle"""
    if not game_state.in_battle:
        raise HTTPException(status_code=400, detail="Not in battle")
    
    player = game_state.player_pokemon
    opponent = game_state.opponent_pokemon
    
    if request.move_index < 0 or request.move_index >= len(player.moves):
        raise HTTPException(status_code=400, detail=f"Invalid move index: {request.move_index}")
    
    turn_results, battle_ended, winner, level_up_msgs = execute_battle_turn(
        player, opponent, request.move_index
    )
    
    game_state.turn += 1
    
    if battle_ended:
        game_state.end_battle()
    
    return BattleMoveResponse(
        turn_results=turn_results,
        player_pokemon=pokemon_to_info(player),
        opponent_pokemon=pokemon_to_info(opponent),
        battle_ended=battle_ended,
        winner=winner,
        level_up_messages=level_up_msgs if level_up_msgs else None
    )


@app.post("/battle/item", response_model=BattleItemResponse)
def use_item(request: UseItemRequest):
    """Use an item in battle"""
    if not game_state.in_battle:
        raise HTTPException(status_code=400, detail="Not in battle")
    
    player = game_state.player_pokemon
    opponent = game_state.opponent_pokemon
    inventory = game_state.inventory
    
    success, message, turn_results, battle_ended, winner = execute_item_turn(
        player, opponent, inventory, request.item_key
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    game_state.turn += 1
    
    if battle_ended:
        game_state.end_battle()
    
    return BattleItemResponse(
        success=success,
        message=message,
        turn_results=turn_results,
        player_pokemon=pokemon_to_info(player),
        opponent_pokemon=pokemon_to_info(opponent),
        inventory=inventory_to_info(inventory),
        battle_ended=battle_ended,
        winner=winner
    )


@app.get("/battle/status", response_model=BattleState)
def get_battle_status():
    """Get current battle status"""
    return BattleState(
        in_battle=game_state.in_battle,
        turn=game_state.turn,
        player_pokemon=pokemon_to_info(game_state.player_pokemon) if game_state.player_pokemon else None,
        opponent_pokemon=pokemon_to_info(game_state.opponent_pokemon) if game_state.opponent_pokemon else None
    )


@app.post("/save", response_model=SaveResponse)
def save_game_state():
    """Save current game state"""
    if not game_state.player_pokemon:
        raise HTTPException(status_code=400, detail="No Pokemon to save")
    
    with capture_output():
        success = save_game(game_state.player_pokemon, game_state.inventory)
    
    return SaveResponse(
        success=success,
        message="Game saved successfully" if success else "Failed to save game"
    )


@app.post("/load", response_model=LoadResponse)
def load_game_state():
    """Load saved game state"""
    with capture_output():
        pokemon, inventory = load_game(ALL_MOVES)
    
    if pokemon and inventory:
        game_state.player_pokemon = pokemon
        game_state.inventory = inventory
        game_state.in_battle = False
        
        return LoadResponse(
            success=True,
            message="Game loaded successfully",
            pokemon=pokemon_to_info(pokemon),
            inventory=inventory_to_info(inventory)
        )
    else:
        return LoadResponse(
            success=False,
            message="No save file found",
            pokemon=None,
            inventory=None
        )


# ============================================
# MULTIPLAYER ENDPOINTS
# ============================================

@app.post("/multiplayer/create-room")
def create_battle_room():
    """Create a new multiplayer battle room"""
    room_id = create_room()
    return {
        "room_id": room_id,
        "message": f"Room {room_id} created"
    }


@app.get("/multiplayer/rooms")
def list_rooms():
    """List all active battle rooms"""
    return {
        "rooms": [
            {
                "room_id": room.room_id,
                "players": sum(1 for p in room.players.values() if p is not None),
                "is_full": room.is_full(),
                "battle_started": room.battle_started
            }
            for room in battle_rooms.values()
        ]
    }


async def broadcast_to_room(room, message: dict, exclude: WebSocket = None):
    """Broadcast a message to all players in a room"""
    for role, player_data in room.players.items():
        if player_data and player_data["websocket"] != exclude:
            try:
                await player_data["websocket"].send_json(message)
            except:
                pass


@app.websocket("/ws/battle/{room_id}")
async def websocket_battle(websocket: WebSocket, room_id: str):
    """WebSocket endpoint for multiplayer battles"""
    await websocket.accept()
    
    room = get_room(room_id)
    if not room:
        await websocket.send_json({"type": "error", "message": f"Room {room_id} not found"})
        await websocket.close()
        return
    
    player_role = room.add_player(websocket, str(id(websocket)))
    if not player_role:
        await websocket.send_json({"type": "error", "message": "Room is full"})
        await websocket.close()
        return
    
    await websocket.send_json({
        "type": "joined",
        "role": player_role.value,
        "room_id": room_id
    })
    
    await broadcast_to_room(room, {"type": "player_joined", "role": player_role.value}, exclude=websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            event_type = message.get("type")
            
            if event_type == "select_pokemon":
                pokemon_name = message.get("pokemon_name")
                pokemon = create_pokemon(pokemon_name)
                
                if not pokemon:
                    await websocket.send_json({"type": "error", "message": f"Invalid Pokemon: {pokemon_name}"})
                    continue
                
                room.set_pokemon(player_role, pokemon)
                
                await broadcast_to_room(room, {
                    "type": "pokemon_selected",
                    "role": player_role.value,
                    "pokemon_name": pokemon_name
                })
                
                if room.both_ready():
                    room.start_battle()
                    await broadcast_to_room(room, {
                        "type": "battle_start",
                        "current_turn": room.current_turn.value,
                        "state": room.get_state()
                    })
            
            elif event_type == "make_move":
                move_index = message.get("move_index")
                result = room.execute_move(player_role, move_index)
                
                if not result["success"]:
                    await websocket.send_json({"type": "error", "message": result["message"]})
                    continue
                
                await broadcast_to_room(room, {
                    "type": "move_result",
                    "result": result,
                    "state": room.get_state()
                })
                
                if result["battle_ended"]:
                    await broadcast_to_room(room, {
                        "type": "battle_end",
                        "winner": result["winner"],
                        "state": room.get_state()
                    })
            
            elif event_type == "get_state":
                await websocket.send_json({"type": "state", "state": room.get_state()})
    
    except WebSocketDisconnect:
        room.remove_player(player_role)
        await broadcast_to_room(room, {
            "type": "player_disconnected",
            "role": player_role.value
        })
        cleanup_empty_rooms()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
