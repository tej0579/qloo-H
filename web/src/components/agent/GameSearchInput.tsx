"use client";

import React, { useState, useEffect, useRef } from "react";
import { searchVideogames } from "@/lib/api";
import { UserGameSelection } from "@/types/agent";
import { Search, Plus, X, Gamepad2, Sparkles, Check } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface GameSearchInputProps {
  selectedGames: UserGameSelection[];
  onSelectGame: (game: UserGameSelection) => void;
  onRemoveGame: (gameId: string) => void;
  onProceed: () => void;
  disabled?: boolean;
}

const PRESET_POPULAR_GAMES = [
  { id: "BAF6317A-DF94-4C90-92AE-63F86560C21B", name: "Elden Ring" },
  { id: "A4B7D201-9988-4F11-AE77-0099118833AA", name: "Cyberpunk 2077" },
  { id: "C7D8E9F0-1122-3344-5566-778899AABBCC", name: "Persona 5" },
  { id: "D1122334-AABB-CCDD-EEFF-001122334455", name: "Baldur's Gate 3" },
  { id: "E2233445-BBCC-DDEE-FFAA-112233445566", name: "Hades" },
];

export const GameSearchInput: React.FC<GameSearchInputProps> = ({
  selectedGames,
  onSelectGame,
  onRemoveGame,
  onProceed,
  disabled,
}) => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Debounced search
  useEffect(() => {
    if (!query.trim() || query.length < 2) {
      setResults([]);
      setIsSearching(false);
      return;
    }

    const timer = setTimeout(async () => {
      setIsSearching(true);
      const res = await searchVideogames(query);
      setResults(res);
      setIsSearching(false);
      setShowDropdown(true);
    }, 250);

    return () => clearTimeout(timer);
  }, [query]);

  // Click outside to close dropdown
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSelect = (item: { id: string; name: string }) => {
    if (selectedGames.some((g) => g.name.toLowerCase() === item.name.toLowerCase())) {
      return;
    }
    if (selectedGames.length >= 3) {
      alert("You can select up to 3 games to blend your taste profile.");
      return;
    }
    onSelectGame({
      id: item.id || `temp-${Date.now()}`,
      name: item.name,
      types: ["urn:entity:videogame"],
    });
    setQuery("");
    setShowDropdown(false);
  };

  return (
    <div className="w-full space-y-4">
      {/* Selected Games Pill Rack */}
      <div className="flex flex-wrap items-center gap-2 min-h-[38px]">
        <span className="text-xs uppercase font-mono text-zinc-500 tracking-wider flex items-center gap-1.5 mr-1">
          <Gamepad2 className="w-3.5 h-3.5 text-cyber-cyan" />
          Active Seeds ({selectedGames.length}/3):
        </span>
        {selectedGames.length === 0 ? (
          <span className="text-xs text-zinc-500 italic">No games selected yet</span>
        ) : (
          selectedGames.map((game) => (
            <div
              key={game.id || game.name}
              className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-cyber-card border border-cyber-cyan/40 text-cyber-cyan text-xs font-semibold shadow-[0_0_10px_rgba(0,240,255,0.15)] animate-in fade-in zoom-in-95 duration-200"
            >
              <span>{game.name}</span>
              <button
                type="button"
                onClick={() => onRemoveGame(game.id || game.name)}
                className="text-zinc-400 hover:text-white hover:bg-zinc-800 rounded p-0.5"
                title="Remove game"
              >
                <X className="w-3 h-3" />
              </button>
            </div>
          ))
        )}
      </div>

      {/* Autocomplete Input Bar */}
      <div className="relative" ref={dropdownRef}>
        <div className="relative flex items-center">
          <Search className="absolute left-4 w-4 h-4 text-zinc-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => query.length >= 2 && setShowDropdown(true)}
            placeholder="Type any video game title (e.g. Elden Ring, Cyberpunk 2077, Death Stranding)..."
            disabled={disabled || selectedGames.length >= 3}
            className="w-full pl-11 pr-28 py-3.5 rounded-xl bg-zinc-900/90 border border-zinc-700/80 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-cyber-cyan focus:ring-1 focus:ring-cyber-cyan shadow-inner-glow transition-all"
          />
          <div className="absolute right-3 flex items-center gap-2">
            {isSearching && (
              <span className="text-xs text-cyber-cyan animate-pulse font-mono">
                Querying Qloo...
              </span>
            )}
            {selectedGames.length > 0 && (
              <button
                onClick={onProceed}
                disabled={disabled}
                className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-cyber-cyan to-blue-600 text-black text-xs font-bold shadow-neon-cyan hover:brightness-110 active:scale-95 transition-all flex items-center gap-1"
              >
                <span>Scout IRL</span>
                <Check className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>

        {/* Autocomplete Dropdown */}
        {showDropdown && results.length > 0 && (
          <div className="absolute z-20 left-0 right-0 mt-2 rounded-xl bg-cyber-card/95 backdrop-blur-xl border border-cyber-border shadow-2xl overflow-hidden divide-y divide-zinc-800/80">
            {results.map((item) => (
              <button
                key={item.id || item.entity_id}
                type="button"
                onClick={() => handleSelect(item)}
                className="w-full px-4 py-3 text-left hover:bg-zinc-800/70 flex items-center justify-between transition-colors group"
              >
                <div className="flex items-center gap-2.5">
                  <Gamepad2 className="w-4 h-4 text-cyber-cyan group-hover:scale-110 transition-transform" />
                  <div>
                    <div className="text-sm font-semibold text-zinc-100 group-hover:text-cyber-cyan transition-colors">
                      {item.name}
                    </div>
                    <div className="text-[11px] text-zinc-500 font-mono">
                      Qloo URN: urn:entity:videogame • UUID: {item.id?.substring(0, 8)}...
                    </div>
                  </div>
                </div>
                <Plus className="w-4 h-4 text-zinc-400 group-hover:text-cyber-cyan" />
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Quick Select Preset Pills */}
      <div className="flex flex-wrap items-center gap-2 pt-1">
        <span className="text-[11px] text-zinc-500 font-mono flex items-center gap-1">
          <Sparkles className="w-3 h-3 text-purple-400" />
          Quick Seeds:
        </span>
        {PRESET_POPULAR_GAMES.map((preset) => {
          const isSelected = selectedGames.some((g) => g.name === preset.name);
          return (
            <button
              key={preset.id}
              type="button"
              disabled={isSelected || selectedGames.length >= 3}
              onClick={() => handleSelect(preset)}
              className={`px-2.5 py-1 rounded-md text-xs font-medium transition-all ${
                isSelected
                  ? "bg-zinc-800 text-zinc-500 border border-zinc-700/50 cursor-default"
                  : "bg-zinc-900/80 text-zinc-300 border border-zinc-800 hover:border-purple-500/50 hover:text-white hover:bg-purple-950/20"
              }`}
            >
              + {preset.name}
            </button>
          );
        })}
      </div>
    </div>
  );
};
