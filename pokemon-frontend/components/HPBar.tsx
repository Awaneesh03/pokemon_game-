'use client';

interface HPBarProps {
    current: number;
    max: number;
}

export default function HPBar({ current, max }: HPBarProps) {
    const percentage = Math.max(0, Math.min(100, (current / max) * 100));

    return (
        <div className="w-full bg-gray-300 rounded-full h-3 overflow-hidden">
            <div
                className={`h-full transition-all duration-500 ${percentage > 50
                        ? 'bg-green-500'
                        : percentage > 25
                            ? 'bg-yellow-500'
                            : 'bg-red-500'
                    }`}
                style={{ width: `${percentage}%` }}
            />
        </div>
    );
}
