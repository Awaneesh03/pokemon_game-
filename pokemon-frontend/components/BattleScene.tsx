'use client';

import type { PokemonInfo } from '@/lib/types';
import PokemonSprite from './PokemonSprite';
import HPBar from './HPBar';
import MoveEffect from './MoveEffect';

interface BattleSceneProps {
    playerPokemon: PokemonInfo;
    opponentPokemon: PokemonInfo;
    animationState: {
        playerAttacking: boolean;
        opponentAttacking: boolean;
        playerHit: boolean;
        opponentHit: boolean;
        currentMove: string | null;
        damage: number;
        effectiveness: number;
        critical: boolean;
    };
}

export default function BattleScene({ playerPokemon, opponentPokemon, animationState }: BattleSceneProps) {
    return (
        <div className="relative bg-gradient-to-b from-sky-300 via-sky-400 to-green-500 rounded-3xl p-8 min-h-[700px] overflow-hidden shadow-2xl border-4 border-white/30">
            {/* Animated Sky Clouds */}
            <div className="absolute top-0 left-0 right-0 h-64 overflow-hidden">
                <div className="absolute top-10 left-20 w-32 h-16 bg-white/40 rounded-full blur-xl animate-pulse"></div>
                <div className="absolute top-20 right-32 w-40 h-20 bg-white/30 rounded-full blur-xl animate-pulse" style={{ animationDelay: '1s' }}></div>
                <div className="absolute top-32 left-1/2 w-36 h-18 bg-white/35 rounded-full blur-xl animate-pulse" style={{ animationDelay: '2s' }}></div>
            </div>

            {/* Sun */}
            <div className="absolute top-8 right-8 w-24 h-24 bg-yellow-300 rounded-full shadow-2xl shadow-yellow-400/50 animate-pulse-glow"></div>

            {/* Grass Ground Pattern */}
            <div className="absolute bottom-0 left-0 right-0 h-48 bg-gradient-to-t from-green-700 to-green-600 opacity-40"></div>
            <div className="absolute bottom-0 left-0 right-0 h-32">
                <div className="absolute bottom-0 left-0 right-0 h-2 bg-green-800 opacity-50"></div>
                <div className="absolute bottom-4 left-0 right-0 h-1 bg-green-900 opacity-30"></div>
            </div>

            {/* Opponent Pokemon (top right) */}
            <div className="absolute top-20 right-32 z-10">
                <div className="mb-6">
                    <div className="glass-dark rounded-2xl p-4 shadow-2xl border-2 border-white/20 min-w-[280px]">
                        <div className="flex justify-between items-center mb-3">
                            <span className="font-black text-2xl text-white drop-shadow-lg">{opponentPokemon.name}</span>
                            <span className="glass px-3 py-1 rounded-full text-sm font-bold text-white">
                                Lv.{opponentPokemon.level}
                            </span>
                        </div>
                        <HPBar current={opponentPokemon.current_hp} max={opponentPokemon.max_hp} />
                        <div className="text-xs text-white/80 mt-2 font-semibold">
                            {opponentPokemon.current_hp} / {opponentPokemon.max_hp} HP
                        </div>
                    </div>
                </div>
                <div className="flex justify-center">
                    <PokemonSprite
                        pokemon={opponentPokemon}
                        isPlayer={false}
                        isAttacking={animationState.opponentAttacking}
                        isHit={animationState.opponentHit}
                    />
                </div>
            </div>

            {/* Player Pokemon (bottom left) */}
            <div className="absolute bottom-32 left-32 z-10">
                <div className="flex justify-center mb-6">
                    <PokemonSprite
                        pokemon={playerPokemon}
                        isPlayer={true}
                        isAttacking={animationState.playerAttacking}
                        isHit={animationState.playerHit}
                    />
                </div>
                <div className="glass-dark rounded-2xl p-4 shadow-2xl border-2 border-white/20 min-w-[280px]">
                    <div className="flex justify-between items-center mb-3">
                        <span className="font-black text-2xl text-white drop-shadow-lg">{playerPokemon.name}</span>
                        <span className="glass px-3 py-1 rounded-full text-sm font-bold text-white">
                            Lv.{playerPokemon.level}
                        </span>
                    </div>
                    <HPBar current={playerPokemon.current_hp} max={playerPokemon.max_hp} />
                    <div className="flex justify-between text-xs text-white/80 mt-2 font-semibold">
                        <span>{playerPokemon.current_hp} / {playerPokemon.max_hp} HP</span>
                        <span>XP: {playerPokemon.xp}/{playerPokemon.level * 100}</span>
                    </div>
                </div>
            </div>

            {/* Move Effects */}
            {animationState.currentMove && (
                <MoveEffect
                    moveName={animationState.currentMove}
                    isPlayerMove={animationState.playerAttacking}
                    damage={animationState.damage}
                    effectiveness={animationState.effectiveness}
                    critical={animationState.critical}
                />
            )}

            {/* Battle Field Lines */}
            <div className="absolute bottom-40 left-0 right-0 h-px bg-white/20"></div>
            <div className="absolute bottom-56 left-0 right-0 h-px bg-white/10"></div>
        </div>
    );
}
