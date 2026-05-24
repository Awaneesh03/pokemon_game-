# Pokemon Battle Game - WebSocket Multiplayer

## WebSocket Multiplayer Features

Real-time multiplayer battles using WebSockets.

### Creating and Joining Rooms

1. **Create a room:**
```bash
curl -X POST http://localhost:8000/multiplayer/create-room
```

Response:
```json
{
  "room_id": "abc123",
  "message": "Room abc123 created"
}
```

2. **List active rooms:**
```bash
curl http://localhost:8000/multiplayer/rooms
```

### WebSocket Connection

Connect to: `ws://localhost:8000/ws/battle/{room_id}`

### WebSocket Events

#### Client → Server

**1. Select Pokemon**
```json
{
  "type": "select_pokemon",
  "pokemon_name": "Pikachu"
}
```

**2. Make Move**
```json
{
  "type": "make_move",
  "move_index": 0
}
```

**3. Get State**
```json
{
  "type": "get_state"
}
```

#### Server → Client

**1. Joined Room**
```json
{
  "type": "joined",
  "role": "player1",
  "room_id": "abc123"
}
```

**2. Pokemon Selected**
```json
{
  "type": "pokemon_selected",
  "role": "player1",
  "pokemon_name": "Pikachu"
}
```

**3. Battle Start**
```json
{
  "type": "battle_start",
  "current_turn": "player1",
  "state": { ... }
}
```

**4. Move Result**
```json
{
  "type": "move_result",
  "result": {
    "attacker": "player1",
    "move": "Thunderbolt",
    "damage": 45,
    "critical": false,
    "effectiveness": 1.0
  },
  "state": { ... }
}
```

**5. Battle End**
```json
{
  "type": "battle_end",
  "winner": "player1",
  "state": { ... }
}
```

## Testing Multiplayer

### Using websocat (CLI tool)

```bash
# Install websocat
brew install websocat  # macOS
# or download from https://github.com/vi/websocat

# Player 1
websocat ws://localhost:8000/ws/battle/abc123

# Player 2 (in another terminal)
websocat ws://localhost:8000/ws/battle/abc123
```

### JavaScript Example

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/battle/abc123');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

// Select Pokemon
ws.send(JSON.stringify({
  type: 'select_pokemon',
  pokemon_name: 'Pikachu'
}));

// Make a move
ws.send(JSON.stringify({
  type: 'make_move',
  move_index: 0
}));
```

## Game Flow

1. Player 1 creates a room
2. Player 2 joins using room ID
3. Both players select Pokemon
4. Battle starts automatically when both ready
5. Players take turns making moves
6. Battle ends when one Pokemon faints
7. Winner is declared

## Features

- ✅ Real-time synchronization
- ✅ Turn-based gameplay
- ✅ Move validation
- ✅ Disconnect handling
- ✅ Room cleanup
- ✅ Type effectiveness
- ✅ Critical hits
- ✅ Damage calculation
