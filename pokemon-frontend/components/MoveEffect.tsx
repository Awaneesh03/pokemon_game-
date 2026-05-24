'use client';

interface MoveEffectProps {
    moveName: string;
    isPlayerMove: boolean;
    damage: number;
    effectiveness: number;
    critical: boolean;
}

export default function MoveEffect({ moveName, isPlayerMove, damage, effectiveness, critical }: MoveEffectProps) {
    const isThunderbolt = moveName.toLowerCase().includes('thunder');
    const isFire =
        moveName.toLowerCase().includes('fire') ||
        moveName.toLowerCase().includes('ember') ||
        moveName.toLowerCase().includes('flame');
    const isWater = moveName.toLowerCase().includes('water') || moveName.toLowerCase().includes('hydro');

    return (
        <div className="absolute inset-0 pointer-events-none">
            {/* Thunderbolt Effect */}
            {isThunderbolt && (
                <div className="absolute inset-0 animate-lightning">
                    <div className="absolute top-0 left-1/2 w-2 h-full bg-yellow-300 transform -translate-x-1/2 animate-pulse"></div>
                    <div className="absolute top-1/4 left-1/3 w-2 h-3/4 bg-yellow-400 transform rotate-12 animate-pulse"></div>
                    <div className="absolute top-1/4 right-1/3 w-2 h-3/4 bg-yellow-400 transform -rotate-12 animate-pulse"></div>
                </div>
            )}

            {/* Fire Effect */}
            {isFire && (
                <div className={`absolute ${isPlayerMove ? 'right-1/4' : 'left-1/4'} top-1/3 animate-fire-burst`}>
                    <div className="text-6xl">🔥</div>
                </div>
            )}

            {/* Water Effect */}
            {isWater && (
                <div className={`absolute ${isPlayerMove ? 'right-1/4' : 'left-1/4'} top-1/3 animate-water-splash`}>
                    <div className="text-6xl">💧</div>
                </div>
            )}

            {/* Damage Number */}
            <div className={`absolute ${isPlayerMove ? 'right-24 top-16' : 'left-24 bottom-24'} animate-damage-float`}>
                <div
                    className={`text-5xl font-black ${critical ? 'text-red-500' : effectiveness > 1 ? 'text-yellow-400' : 'text-white'
                        } drop-shadow-lg`}
                >
                    -{damage}
                    {critical && <span className="text-3xl ml-2">💥</span>}
                </div>
            </div>

            {/* Effectiveness Stars */}
            {effectiveness > 1 && (
                <div className={`absolute ${isPlayerMove ? 'right-32 top-24' : 'left-32 bottom-32'}`}>
                    <div className="text-4xl animate-star-burst">⭐</div>
                </div>
            )}
        </div>
    );
}
