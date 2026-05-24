# Pokemon Battle Game - FastAPI Backend

## Running the API

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
cd "pokemon game"
python -m uvicorn api.main:app --reload
```

3. Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### GET /pokemon
List all available Pokemon with stats and starting moves.

### POST /select-pokemon
Select your starting Pokemon.
```json
{
  "pokemon_name": "Pikachu"
}
```

### POST /battle/start
Start a battle against an opponent.
```json
{
  "opponent_name": "Charmander"
}
```

### POST /battle/move
Use a move in battle.
```json
{
  "move_index": 0
}
```

### POST /battle/item
Use an item in battle.
```json
{
  "item_key": "potion"
}
```

### GET /battle/status
Get current battle state.

### POST /save
Save current game state.

### POST /load
Load saved game state.

## Example Usage

```bash
# 1. List available Pokemon
curl http://localhost:8000/pokemon

# 2. Select Pikachu
curl -X POST http://localhost:8000/select-pokemon \
  -H "Content-Type: application/json" \
  -d '{"pokemon_name": "Pikachu"}'

# 3. Start battle
curl -X POST http://localhost:8000/battle/start \
  -H "Content-Type: application/json" \
  -d '{"opponent_name": "Charmander"}'

# 4. Use move
curl -X POST http://localhost:8000/battle/move \
  -H "Content-Type: application/json" \
  -d '{"move_index": 0}'

# 5. Check status
curl http://localhost:8000/battle/status

# 6. Save game
curl -X POST http://localhost:8000/save
```
