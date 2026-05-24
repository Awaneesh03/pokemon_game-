// API client for Pokemon Battle Game backend

import type {
    AvailablePokemon,
    PokemonInfo,
    InventoryInfo,
    BattleState,
    BattleMoveResponse,
} from './types';

const API_BASE_URL = 'http://localhost:8000';

class PokemonAPI {
    private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers,
            },
            ...options,
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }

        return response.json();
    }

    async getAvailablePokemon(): Promise<AvailablePokemon[]> {
        const data = await this.request<{ pokemon: AvailablePokemon[] }>('/pokemon');
        return data.pokemon;
    }

    async selectPokemon(pokemonName: string): Promise<{ pokemon: PokemonInfo; inventory: InventoryInfo }> {
        return this.request('/select-pokemon', {
            method: 'POST',
            body: JSON.stringify({ pokemon_name: pokemonName }),
        });
    }

    async startBattle(opponentName: string): Promise<{ player_pokemon: PokemonInfo; opponent_pokemon: PokemonInfo }> {
        return this.request('/battle/start', {
            method: 'POST',
            body: JSON.stringify({ opponent_name: opponentName }),
        });
    }

    async useMove(moveIndex: number): Promise<BattleMoveResponse> {
        return this.request('/battle/move', {
            method: 'POST',
            body: JSON.stringify({ move_index: moveIndex }),
        });
    }

    async getBattleStatus(): Promise<BattleState> {
        return this.request('/battle/status');
    }

    async saveGame(): Promise<{ success: boolean; message: string }> {
        return this.request('/save', { method: 'POST' });
    }

    async loadGame(): Promise<{ success: boolean; pokemon: PokemonInfo | null; inventory: InventoryInfo | null }> {
        return this.request('/load', { method: 'POST' });
    }
}

export const api = new PokemonAPI();
