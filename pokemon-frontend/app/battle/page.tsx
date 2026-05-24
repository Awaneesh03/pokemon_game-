'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import type { PokemonInfo } from '@/lib/types';

export default function BattlePage() {
    const router = useRouter();
    const [playerPokemon, setPlayerPokemon] = useState<PokemonInfo | null>(null);
    const [opponentPokemon, setOpponentPokemon] = useState<PokemonInfo | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [battleEnded, setBattleEnded] = useState(false);
    const [winner, setWinner] = useState<string | null>(null);
    const [message, setMessage] = useState<string>('');

    useEffect(() => {
        loadBattleStatus();
    }, []);

    const loadBattleStatus = async () => {
        try {
            const status = await api.getBattleStatus();
            if (status.player_pokemon) {
                setPlayerPokemon(status.player_pokemon);
            } else {
                router.push('/');
                return;
            }
            if (status.opponent_pokemon) {
                setOpponentPokemon(status.opponent_pokemon);
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load battle');
        }
    };

    const startBattle = async (opponentName: string) => {
        try {
            setLoading(true);
            setError(null);
            const result = await api.startBattle(opponentName);
            setPlayerPokemon(result.player_pokemon);
            setOpponentPokemon(result.opponent_pokemon);
            setMessage(`Battle started against ${opponentName}!`);
            setBattleEnded(false);
            setWinner(null);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to start battle');
        } finally {
            setLoading(false);
        }
    };

    const useMove = async (moveIndex: number) => {
        if (!playerPokemon || !opponentPokemon || loading) return;

        try {
            setLoading(true);
            setError(null);
            const result = await api.useMove(moveIndex);

            setPlayerPokemon(result.player_pokemon);
            setOpponentPokemon(result.opponent_pokemon);

            const messages = result.turn_results.map((r) => r.message).join(' ');
            setMessage(messages);

            if (result.battle_ended) {
                setBattleEnded(true);
                setWinner(result.winner);
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to use move');
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        try {
            const result = await api.saveGame();
            setMessage(result.message);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to save');
        }
    };

    const handleLoad = async () => {
        try {
            const result = await api.loadGame();
            if (result.success && result.pokemon) {
                setPlayerPokemon(result.pokemon);
                setOpponentPokemon(null);
                setBattleEnded(false);
                setMessage('Game loaded!');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load');
        }
    };

    const getPokemonSprite = (name: string, isBack: boolean = false): string => {
        const pokemonIds: Record<string, number> = {
            'Pikachu': 25,
            'Charmander': 4,
            'Squirtle': 7,
            'Bulbasaur': 1,
        };
        const id = pokemonIds[name] || 1;
        const type = isBack ? 'back' : 'front';
        return `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${type}/${id}.png`;
    };

    const getHPPercentage = (current: number, max: number): number => {
        return Math.max(0, Math.min(100, (current / max) * 100));
    };

    const getHPColor = (percentage: number): string => {
        if (percentage > 50) return 'bg-green-500';
        if (percentage > 25) return 'bg-yellow-500';
        return 'bg-red-500';
    };

    const getMoveTypeColor = (type: string): string => {
        const colors: Record<string, string> = {
            Electric: 'bg-yellow-500 hover:bg-yellow-600',
            Fire: 'bg-orange-500 hover:bg-orange-600',
            Water: 'bg-blue-500 hover:bg-blue-600',
            Grass: 'bg-green-500 hover:bg-green-600',
            Normal: 'bg-gray-500 hover:bg-gray-600',
        };
        return colors[type] || 'bg-purple-500 hover:bg-purple-600';
    };

    if (!playerPokemon) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-blue-400 to-blue-600">
                <div className="text-white text-2xl font-bold">Loading...</div>
            </div>
        );
    }

    return (
        <main className="min-h-screen bg-gradient-to-b from-blue-400 to-blue-600 p-4">
            <div className="max-w-6xl mx-auto">
                {/* Top Bar */}
                <div className="flex justify-between items-center mb-4">
                    <h1 className="text-3xl font-bold text-white">Battle Arena</h1>
                    <div className="flex gap-2">
                        <button
                            onClick={handleSave}
                            className="bg-blue-700 hover:bg-blue-800 text-white px-4 py-2 rounded-lg font-semibold"
                        >
                            Save
                        </button>
                        <button
                            onClick={handleLoad}
                            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-semibold"
                        >
                            Load
                        </button>
                    </div>
                </div>

                {error && (
                    <div className="bg-red-100 border-2 border-red-400 rounded-lg p-3 mb-4">
                        <p className="text-red-800 font-semibold">{error}</p>
                    </div>
                )}

                {/* Opponent Selection */}
                {!opponentPokemon && !battleEnded && (
                    <div className="bg-white rounded-xl p-6 mb-4 shadow-lg">
                        <h2 className="text-2xl font-bold text-gray-800 mb-4">Choose Your Opponent</h2>
                        <div className="grid grid-cols-3 gap-4">
                            {['Pikachu', 'Charmander', 'Squirtle', 'Bulbasaur']
                                .filter((name) => name !== playerPokemon.name)
                                .map((name) => (
                                    <button
                                        key={name}
                                        onClick={() => startBattle(name)}
                                        disabled={loading}
                                        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition-colors disabled:bg-gray-400"
                                    >
                                        {name}
                                    </button>
                                ))}
                        </div>
                    </div>
                )}

                {/* Battle Screen */}
                {opponentPokemon && !battleEnded && (
                    <div className="space-y-4">
                        {/* Battle Area */}
                        <div className="bg-green-100 rounded-xl p-8 min-h-[500px] relative shadow-lg">
                            {/* Opponent Pokemon - Top Right */}
                            <div className="absolute top-8 right-8">
                                <img
                                    src={getPokemonSprite(opponentPokemon.name, false)}
                                    alt={opponentPokemon.name}
                                    className="w-48 h-48"
                                />
                            </div>

                            {/* Opponent Info - Top Left */}
                            <div className="absolute top-8 left-8 bg-white rounded-lg p-4 shadow-md w-64">
                                <div className="flex justify-between items-center mb-2">
                                    <h3 className="text-xl font-bold text-gray-800">{opponentPokemon.name}</h3>
                                    <span className="text-sm text-gray-600">Lv.{opponentPokemon.level}</span>
                                </div>
                                <div className="mb-1">
                                    <div className="flex justify-between text-xs mb-1">
                                        <span>HP</span>
                                        <span>
                                            {opponentPokemon.current_hp}/{opponentPokemon.max_hp}
                                        </span>
                                    </div>
                                    <div className="w-full bg-gray-300 rounded-full h-3">
                                        <div
                                            className={`h-3 rounded-full transition-all duration-500 ${getHPColor(
                                                getHPPercentage(opponentPokemon.current_hp, opponentPokemon.max_hp)
                                            )}`}
                                            style={{ width: `${getHPPercentage(opponentPokemon.current_hp, opponentPokemon.max_hp)}%` }}
                                        />
                                    </div>
                                </div>
                            </div>

                            {/* Player Pokemon - Bottom Left */}
                            <div className="absolute bottom-8 left-8">
                                <img
                                    src={getPokemonSprite(playerPokemon.name, true)}
                                    alt={playerPokemon.name}
                                    className="w-48 h-48"
                                />
                            </div>

                            {/* Player Info - Bottom Right */}
                            <div className="absolute bottom-8 right-8 bg-white rounded-lg p-4 shadow-md w-64">
                                <div className="flex justify-between items-center mb-2">
                                    <h3 className="text-xl font-bold text-gray-800">{playerPokemon.name}</h3>
                                    <span className="text-sm text-gray-600">Lv.{playerPokemon.level}</span>
                                </div>
                                <div className="mb-1">
                                    <div className="flex justify-between text-xs mb-1">
                                        <span>HP</span>
                                        <span>
                                            {playerPokemon.current_hp}/{playerPokemon.max_hp}
                                        </span>
                                    </div>
                                    <div className="w-full bg-gray-300 rounded-full h-3">
                                        <div
                                            className={`h-3 rounded-full transition-all duration-500 ${getHPColor(
                                                getHPPercentage(playerPokemon.current_hp, playerPokemon.max_hp)
                                            )}`}
                                            style={{ width: `${getHPPercentage(playerPokemon.current_hp, playerPokemon.max_hp)}%` }}
                                        />
                                    </div>
                                </div>
                                <div className="text-xs text-gray-600">
                                    XP: {playerPokemon.xp}/{playerPokemon.level * 100}
                                </div>
                            </div>
                        </div>

                        {/* Move Buttons */}
                        <div className="bg-white rounded-xl p-6 shadow-lg">
                            <h3 className="text-xl font-bold text-gray-800 mb-4">Your Moves</h3>
                            <div className="grid grid-cols-2 gap-4">
                                {playerPokemon.moves.map((move, index) => (
                                    <button
                                        key={index}
                                        onClick={() => useMove(index)}
                                        disabled={loading}
                                        className={`${getMoveTypeColor(
                                            move.type
                                        )} text-white font-bold py-4 px-6 rounded-lg transition-colors disabled:bg-gray-400`}
                                    >
                                        <div className="text-left">
                                            <div className="text-lg">{move.name}</div>
                                            <div className="text-sm opacity-90">
                                                {move.type} • PWR: {move.power}
                                            </div>
                                        </div>
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* Message Box */}
                        {message && (
                            <div className="bg-white rounded-xl p-4 shadow-lg">
                                <p className="text-gray-800">{message}</p>
                            </div>
                        )}
                    </div>
                )}

                {/* Battle End */}
                {battleEnded && (
                    <div className="bg-white rounded-xl p-12 text-center shadow-lg">
                        <h2 className="text-5xl font-bold mb-6 text-gray-800">
                            {winner === playerPokemon.name ? '🎉 Victory!' : '💀 Defeat!'}
                        </h2>
                        <p className="text-2xl mb-8 text-gray-700">{winner} wins!</p>
                        <button
                            onClick={() => {
                                setOpponentPokemon(null);
                                setBattleEnded(false);
                                setWinner(null);
                                setMessage('');
                            }}
                            className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-4 rounded-lg"
                        >
                            New Battle
                        </button>
                    </div>
                )}
            </div>
        </main>
    );
}
