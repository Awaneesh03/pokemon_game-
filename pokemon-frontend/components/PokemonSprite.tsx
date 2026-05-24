'use client';

import type { PokemonInfo } from '@/lib/types';

interface PokemonSpriteProps {
    pokemon: PokemonInfo;
    isPlayer: boolean;
    isAttacking: boolean;
    isHit: boolean;
}

const POKEMON_EMOJI: Record<string, string> = {
    Pikachu: '⚡',
    Charmander: '🔥',
    Squirtle: '💧',
    Bulbasaur: '🌿',
};

const POKEMON_COLORS: Record<string, string> = {
    Electric: 'from-yellow-400 via-yellow-500 to-amber-600',
    Fire: 'from-red-500 via-orange-500 to-red-700',
    Water: 'from-blue-500 via-cyan-500 to-blue-700',
    Grass: 'from-green-500 via-emerald-500 to-green-700',
};

export default function PokemonSprite({ pokemon, isPlayer, isAttacking, isHit }: PokemonSpriteProps) {
    const emoji = POKEMON_EMOJI[pokemon.name] || '❓';
    const colorGradient = POKEMON_COLORS[pokemon.type] || 'from-gray-400 to-gray-600';
    const isFainted = pokemon.current_hp <= 0;

    const getAnimationClass = () => {
        if (isFainted) return 'animate-faint';
        if (isAttacking) return isPlayer ? 'animate-attack-forward' : 'animate-attack-backward';
        if (isHit) return 'animate-hit-shake';
        return 'animate-idle-float';
    };

    return (
        <div className={`relative ${getAnimationClass()}`}>
            {/* Outer Glow Ring */}
            <div className={`absolute inset-0 rounded-full bg-gradient-to-br ${colorGradient} opacity-30 blur-2xl scale-110 ${!isFainted && 'animate-pulse'}`}></div>

            {/* Pokemon Circle */}
            <div
                className={`
        relative w-48 h-48 rounded-full bg-gradient-to-br ${colorGradient}
        flex items-center justify-center shadow-2xl
        ${isFainted ? 'opacity-20 grayscale' : ''}
        ${isHit ? 'brightness-200' : ''}
        transition-all duration-200
        border-4 border-white/30
      `}
            >
                {/* Inner Glow */}
                <div className={`absolute inset-4 rounded-full bg-gradient-to-br ${colorGradient} opacity-50 blur-md`}></div>

                {/* Pokemon Emoji */}
                <div className={`relative z-10 text-9xl filter drop-shadow-2xl ${isPlayer ? '' : 'scale-x-[-1]'}`}>
                    {emoji}
                </div>

                {/* Shimmer Effect */}
                {!isFainted && !isHit && (
                    <div className="absolute inset-0 rounded-full overflow-hidden">
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
                    </div>
                )}

                {/* Attack Charge Effect */}
                {isAttacking && (
                    <div className="absolute inset-0 rounded-full bg-white/40 animate-pulse-glow"></div>
                )}
            </div>

            {/* Fainted Stars */}
            {isFainted && (
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 pointer-events-none">
                    <div className="text-8xl animate-spin">💫</div>
                    <div className="text-5xl font-black text-red-600 drop-shadow-lg mt-4 text-center animate-pulse">
                        FAINTED
                    </div>
                </div>
            )}

            {/* Level Badge */}
            <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2">
                <div className="glass-dark px-4 py-2 rounded-full border-2 border-white/30 shadow-xl">
                    <span className="text-white font-bold text-sm">Lv. {pokemon.level}</span>
                </div>
            </div>
        </div>
    );
}
