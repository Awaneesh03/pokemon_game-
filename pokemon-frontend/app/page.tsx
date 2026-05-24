'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import type { AvailablePokemon } from '@/lib/types';

export default function Home() {
  const router = useRouter();
  const [pokemon, setPokemon] = useState<AvailablePokemon[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadPokemon();
  }, []);

  const loadPokemon = async () => {
    try {
      setLoading(true);
      const data = await api.getAvailablePokemon();
      setPokemon(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load Pokemon');
    } finally {
      setLoading(false);
    }
  };

  const handleChoosePokemon = async (pokemonName: string) => {
    try {
      setLoading(true);
      await api.selectPokemon(pokemonName);
      router.push('/battle');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to select Pokemon');
      setLoading(false);
    }
  };

  const getPokemonSprite = (name: string): string => {
    const pokemonIds: Record<string, number> = {
      'Pikachu': 25,
      'Charmander': 4,
      'Squirtle': 7,
      'Bulbasaur': 1,
    };
    const id = pokemonIds[name] || 1;
    return `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${id}.png`;
  };

  const getTypeColor = (type: string): string => {
    const colors: Record<string, string> = {
      Electric: 'bg-yellow-400',
      Fire: 'bg-orange-500',
      Water: 'bg-blue-500',
      Grass: 'bg-green-500',
    };
    return colors[type] || 'bg-gray-500';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-blue-400 to-blue-600">
        <div className="text-white text-2xl font-bold">Loading...</div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-400 to-blue-600 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-5xl font-bold text-white text-center mb-2">Pokemon Battle</h1>
        <p className="text-white text-center mb-8">Choose your Pokemon</p>

        {error && (
          <div className="max-w-md mx-auto mb-6 bg-red-100 border-2 border-red-400 rounded-lg p-4">
            <p className="text-red-800 text-center font-semibold">{error}</p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {pokemon.map((p) => (
            <div key={p.name} className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="bg-gray-100 p-6">
                <img
                  src={getPokemonSprite(p.name)}
                  alt={p.name}
                  className="w-full h-40 object-contain"
                />
              </div>

              <div className="p-4">
                <div className="flex items-center justify-between mb-3">
                  <h2 className="text-2xl font-bold text-gray-800">{p.name}</h2>
                  <span className={`${getTypeColor(p.type)} text-white px-3 py-1 rounded-full text-sm font-semibold`}>
                    {p.type}
                  </span>
                </div>

                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600 font-medium">HP</span>
                    <span className="font-bold text-gray-800">{p.base_stats.hp}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600 font-medium">Attack</span>
                    <span className="font-bold text-gray-800">{p.base_stats.attack}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600 font-medium">Defense</span>
                    <span className="font-bold text-gray-800">{p.base_stats.defense}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600 font-medium">Speed</span>
                    <span className="font-bold text-gray-800">{p.base_stats.speed}</span>
                  </div>
                </div>

                <div className="mb-4">
                  <p className="text-xs text-gray-500 font-semibold mb-2">Starting Moves:</p>
                  <div className="flex flex-wrap gap-1">
                    {p.starting_moves.map((move) => (
                      <span key={move} className="bg-gray-200 text-gray-700 px-2 py-1 rounded text-xs">
                        {move}
                      </span>
                    ))}
                  </div>
                </div>

                <button
                  onClick={() => handleChoosePokemon(p.name)}
                  disabled={loading}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition-colors disabled:bg-gray-400"
                >
                  Choose Pokemon
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
