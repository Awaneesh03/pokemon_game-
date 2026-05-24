'use client';

import type { MoveInfo } from '@/lib/types';

interface MoveButtonProps {
    move: MoveInfo;
    index: number;
    onUseMove: (index: number) => void;
    disabled: boolean;
}

export default function MoveButton({ move, index, onUseMove, disabled }: MoveButtonProps) {
    const typeColors: Record<string, string> = {
        Electric: 'from-yellow-400 via-yellow-500 to-amber-600',
        Fire: 'from-red-500 via-orange-500 to-red-700',
        Water: 'from-blue-500 via-cyan-500 to-blue-700',
        Grass: 'from-green-500 via-emerald-500 to-green-700',
        Normal: 'from-gray-500 via-gray-600 to-gray-700',
    };

    const colorClass = typeColors[move.type] || 'from-purple-500 via-purple-600 to-purple-700';

    return (
        <button
            onClick={() => onUseMove(index)}
            disabled={disabled}
            className={`group relative bg-gradient-to-br ${colorClass} text-white px-8 py-6 rounded-2xl font-bold disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-2xl hover:shadow-3xl transform hover:scale-105 active:scale-95 border-2 border-white/30 overflow-hidden`}
        >
            {/* Shimmer Effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent group-hover:animate-shimmer"></div>

            {/* Glow Effect */}
            <div className={`absolute inset-0 bg-gradient-to-br ${colorClass} opacity-0 group-hover:opacity-50 blur-xl transition-opacity`}></div>

            <div className="relative z-10 text-left">
                <div className="text-xl font-black mb-1 drop-shadow-lg">{move.name}</div>
                <div className="flex gap-4 text-xs font-semibold opacity-90">
                    <span className="glass-dark px-2 py-1 rounded">{move.type}</span>
                    <span className="glass-dark px-2 py-1 rounded">⚡ {move.power}</span>
                    <span className="glass-dark px-2 py-1 rounded">🎯 {move.accuracy}%</span>
                </div>
            </div>

            {/* Corner Accent */}
            <div className="absolute top-0 right-0 w-16 h-16 bg-white/10 rounded-bl-full"></div>
        </button>
    );
}
