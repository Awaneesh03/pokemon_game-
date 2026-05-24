"""
FastAPI Pokemon Battle Game - WebSocket Multiplayer Endpoints
Add these routes to api/main.py
"""

from fastapi import WebSocket, WebSocketDisconnect
import json
from api.multiplayer import (
    battle_rooms, create_room, get_room, cleanup_empty_rooms,
    PlayerRole
)
from api.services import create_pokemon


# Add these endpoints to your main.py app

@app.post("/multiplayer/create-room")
def create_battle_room():
    """Create a new multiplayer battle room"""
    room_id = create_room()
    return {
        "room_id": room_id,
        "message": f"Room {room_id} created. Share this ID with your opponent!"
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


@app.websocket("/ws/battle/{room_id}")
async def websocket_battle(websocket: WebSocket, room_id: str):
    """
    WebSocket endpoint for multiplayer battles.
    
    Events:
    - join_room: Join the battle room
    - select_pokemon: Select your Pokemon
    - make_move: Make a move (move_index)
    - get_state: Request current battle state
    """
    await websocket.accept()
    
    room = get_room(room_id)
    if not room:
        await websocket.send_json({
            "type": "error",
            "message": f"Room {room_id} not found"
        })
        await websocket.close()
        return
    
    # Add player to room
    player_role = room.add_player(websocket, str(id(websocket)))
    if not player_role:
        await websocket.send_json({
            "type": "error",
            "message": "Room is full"
        })
        await websocket.close()
        return
    
    # Send join confirmation
    await websocket.send_json({
        "type": "joined",
        "role": player_role.value,
        "room_id": room_id,
        "message": f"Joined as {player_role.value}"
    })
    
    # Broadcast to other player
    await broadcast_to_room(room, {
        "type": "player_joined",
        "role": player_role.value
    }, exclude=websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            event_type = message.get("type")
            
            if event_type == "select_pokemon":
                # Player selects Pokemon
                pokemon_name = message.get("pokemon_name")
                pokemon = create_pokemon(pokemon_name)
                
                if not pokemon:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Invalid Pokemon: {pokemon_name}"
                    })
                    continue
                
                room.set_pokemon(player_role, pokemon)
                
                # Broadcast to room
                await broadcast_to_room(room, {
                    "type": "pokemon_selected",
                    "role": player_role.value,
                    "pokemon_name": pokemon_name
                })
                
                # If both ready, start battle
                if room.both_ready():
                    room.start_battle()
                    await broadcast_to_room(room, {
                        "type": "battle_start",
                        "current_turn": room.current_turn.value,
                        "state": room.get_state()
                    })
            
            elif event_type == "make_move":
                # Player makes a move
                move_index = message.get("move_index")
                
                result = room.execute_move(player_role, move_index)
                
                if not result["success"]:
                    await websocket.send_json({
                        "type": "error",
                        "message": result["message"]
                    })
                    continue
                
                # Broadcast move result to both players
                await broadcast_to_room(room, {
                    "type": "move_result",
                    "result": result,
                    "state": room.get_state()
                })
                
                # If battle ended, send end message
                if result["battle_ended"]:
                    await broadcast_to_room(room, {
                        "type": "battle_end",
                        "winner": result["winner"],
                        "state": room.get_state()
                    })
            
            elif event_type == "get_state":
                # Send current state
                await websocket.send_json({
                    "type": "state",
                    "state": room.get_state()
                })
    
    except WebSocketDisconnect:
        # Player disconnected
        room.remove_player(player_role)
        
        # Notify other player
        await broadcast_to_room(room, {
            "type": "player_disconnected",
            "role": player_role.value,
            "message": f"{player_role.value} disconnected"
        })
        
        # Clean up empty rooms
        cleanup_empty_rooms()


async def broadcast_to_room(room, message: dict, exclude: WebSocket = None):
    """Broadcast a message to all players in a room"""
    for role, player_data in room.players.items():
        if player_data and player_data["websocket"] != exclude:
            try:
                await player_data["websocket"].send_json(message)
            except:
                pass  # Player disconnected
