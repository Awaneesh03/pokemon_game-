<div align="center">

# ⚔️ Pokémon Battle Game

**A full-stack Pokémon battle game: Python game engine, FastAPI REST + WebSocket API, and two frontends (Next.js and vanilla JS). Single-player, tournament and real-time multiplayer.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![WebSockets](https://img.shields.io/badge/WebSockets-010101?style=flat-square)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)

[Features](#features) · [Tech Stack](#tech-stack) · [Getting Started](#getting-started) · [API Reference](#api-reference)

</div>

---

## Features

### Battle System
- Turn-based battles with **speed-based turn order**
- **Type effectiveness** — Fire beats Grass, Grass beats Water, Water beats Fire, Electric beats Water
- **Critical hits** — 10% chance for 1.5× damage
- Smart AI opponent that prioritizes super-effective and high-damage moves (with 15% randomness to keep it unpredictable)

### Pokemon & Progression
- 4 Pokemon: **Pikachu** (Electric), **Charmander** (Fire), **Squirtle** (Water), **Bulbasaur** (Grass)
- Each Pokemon has HP, Attack, Defense, Speed, Level, and XP
- Gain 50 XP per win — level up when XP ≥ Level × 100
- Stats increase on level-up; HP fully restored
- Learn new moves as you level up (choose which move to replace when you know 4)

### Items
| Item | Effect | Starting Quantity |
|------|--------|:-----------------:|
| Potion | +30 HP | 3 |
| Super Potion | +60 HP | 2 |
| Revive | Revive fainted Pokemon at 50% HP | 1 |

### Game Modes
- **Single Battle** — pick a Pokemon, fight an opponent
- **Tournament Mode** — 3-round gauntlet with escalating difficulty (Bulbasaur L1 → Squirtle L3 → Charmander L5)
- **Multiplayer** — real-time WebSocket battles between two players in shared rooms

### Save / Load
- Save and load your Pokemon's stats, level, XP, moves, and inventory
- JSON-based persistence (`save_game.json`)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Core game logic | Python 3 |
| API | FastAPI + Uvicorn |
| Real-time multiplayer | WebSockets (FastAPI native) |
| Data validation | Pydantic |
| React frontend | Next.js 14 + TypeScript + Tailwind CSS |
| Vanilla JS UI | Plain HTML/CSS/JS (no build step) |

---

## Project Structure

```
pokemon game/
├── pokemon.py           # Pokemon class (stats, leveling, fainting)
├── move.py              # Move class (type, power, accuracy)
├── battle.py            # Battle engine, damage calc, AI logic
├── tournament.py        # Tournament mode (CLI)
├── items.py             # Item definitions and Inventory class
├── learnsets.py         # Move learnsets per Pokemon per level
├── save_load.py         # JSON save/load system
├── main.py              # Integration entry point
├── requirements.txt
│
├── api/
│   ├── main.py          # FastAPI app — REST endpoints + WebSocket
│   ├── models.py        # Pydantic request/response models
│   ├── services.py      # Business logic wrapping core game code
│   ├── multiplayer.py   # WebSocket room and battle management
│   └── state.py         # Global game state
│
├── pokemon-frontend/    # Next.js React app
│   ├── app/
│   │   ├── page.tsx         # Pokemon selection screen
│   │   └── battle/page.tsx  # Battle interface
│   ├── components/      # BattleScene, HPBar, MoveButton, etc.
│   └── lib/
│       ├── api.ts           # API client
│       └── types.ts         # TypeScript type definitions
│
├── playable-ui/
│   └── index.html       # Standalone vanilla JS UI
│
└── test_*.py            # Test files (battle, items, leveling, AI, etc.)
```

---

## Getting Started

### 1. Backend API

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn api.main:app --reload
```

- API runs at: `http://localhost:8000`
- Interactive API docs: `http://localhost:8000/docs`

### 2. Next.js Frontend

```bash
cd pokemon-frontend
npm install
npm run dev
```

Opens at `http://localhost:3000` — connects to the backend API automatically.

### 3. Vanilla JS UI (no install needed)

Open `playable-ui/index.html` directly in your browser. It connects to the API at `http://127.0.0.1:8001`.

> Make sure to start the backend on port 8001 if using the vanilla UI:
> ```bash
> uvicorn api.main:app --reload --port 8001
> ```

### 4. Tournament Mode (CLI)

```bash
python tournament.py
```

A menu-driven terminal experience — choose your Pokemon, fight 3 opponents, save between rounds.

---

## API Reference

### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API info |
| `GET` | `/pokemon` | List all available Pokemon with stats |
| `POST` | `/select-pokemon` | Select your Pokemon `{ "pokemon_name": "Pikachu" }` |
| `POST` | `/battle/start` | Start a battle `{ "opponent_name": "Charmander" }` |
| `POST` | `/battle/move` | Use a move `{ "move_index": 0 }` |
| `POST` | `/battle/item` | Use an item `{ "item_key": "potion" }` |
| `GET` | `/battle/status` | Get current battle state |
| `POST` | `/save` | Save game |
| `POST` | `/load` | Load game |
| `POST` | `/multiplayer/create-room` | Create a multiplayer room |
| `GET` | `/multiplayer/rooms` | List active rooms |

### WebSocket — Multiplayer

Connect to: `ws://localhost:8000/ws/{room_id}`

**Send:**
```json
{ "type": "select_pokemon", "pokemon_name": "Pikachu" }
{ "type": "make_move", "move_index": 0 }
{ "type": "get_state" }
```

**Receive:**
```json
{ "type": "joined", "role": "player1", "room_id": "abc123" }
{ "type": "battle_start", "current_turn": "player1", "state": { ... } }
{ "type": "move_result", "result": { ... }, "state": { ... } }
{ "type": "battle_end", "winner": "player1", "state": { ... } }
{ "type": "player_disconnected", "role": "player2" }
```

---

## Game Mechanics

### Damage Formula
```
Damage = (Move Power + Attacker Attack − Defender Defense) × Type Multiplier × Crit Multiplier
```

### Type Chart
| Attacker | Defender | Multiplier |
|----------|----------|:----------:|
| Fire | Grass | 2× |
| Grass | Water | 2× |
| Water | Fire | 2× |
| Electric | Water | 2× |
| Anything else | — | 1× |

### Leveling
```
Level up when: XP >= Level × 100
Stat gains:    HP +10 · Attack +5 · Defense +3 · Speed +2
```

---

## 👤 Author

**Awaneesh Gupta** — B.Tech CSE (AI) @ Vedam School of Technology

[![GitHub](https://img.shields.io/badge/GitHub-Awaneesh03-181717?style=flat-square&logo=github)](https://github.com/Awaneesh03)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-awaneesh--gupta-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/awaneesh-gupta)

<p align="center"><sub>If you found this project useful, consider giving it a ⭐</sub></p>
