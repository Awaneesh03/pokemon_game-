// TypeScript types for Pokemon Battle Game API

export interface MoveInfo {
    name: string;
    type: string;
    power: number;
    accuracy: number;
}

export interface PokemonStats {
    hp: number;
    attack: number;
    defense: number;
    speed: number;
}

export interface PokemonInfo {
    name: string;
    type: string;
    level: number;
    xp: number;
    current_hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
    moves: MoveInfo[];
}

export interface InventoryInfo {
    potion: number;
    super_potion: number;
    revive: number;
}

export interface AvailablePokemon {
    name: string;
    type: string;
    base_stats: PokemonStats;
    starting_moves: string[];
}

export interface TurnResult {
    attacker: string;
    move: string;
    damage: number;
    critical: boolean;
    effectiveness: number;
    message: string;
}

export interface BattleState {
    in_battle: boolean;
    turn: number;
    player_pokemon: PokemonInfo | null;
    opponent_pokemon: PokemonInfo | null;
}

export interface BattleMoveResponse {
    turn_results: TurnResult[];
    player_pokemon: PokemonInfo;
    opponent_pokemon: PokemonInfo;
    battle_ended: boolean;
    winner: string | null;
    level_up_messages: string[] | null;
}
