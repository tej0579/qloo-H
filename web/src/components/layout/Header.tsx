"use client";

import React, { useEffect, useState } from "react";
import Image from "next/image";
import { fetchHealth } from "@/lib/api";
import { Sparkles, Terminal, Github, ExternalLink, Activity } from "lucide-react";

interface HeaderProps {
  activeView: "agent" | "dashboard";
  onViewChange: (view: "agent" | "dashboard") => void;
  hasLootDrop: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  activeView,
  onViewChange,
  hasLootDrop,
}) => {
  const [health, setHealth] = useState<{
    status: string;
    qloo_connected: boolean;
    qloo_latency_ms?: number;
  }>({ status: "checking", qloo_connected: false });

  useEffect(() => {
    fetchHealth().then(setHealth);
    const interval = setInterval(() => {
      fetchHealth().then(setHealth);
    }, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-cyber-border/80 bg-cyber-dark/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand & Symbol */}
        <div className="flex items-center gap-3">
          <div className="relative w-9 h-9 flex items-center justify-center rounded-lg bg-cyber-card border border-cyber-cyan/40 shadow-neon-cyan/20">
            <Image
              src="/lootdrop-symbol.svg"
              alt="LootDrop"
              width={26}
              height={26}
              className="drop-shadow-[0_0_8px_rgba(0,240,255,0.7)]"
            />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-cyber-cyan via-purple-300 to-cyber-pink">
                IRL LOOTDROP
              </span>
              <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700">
                v1.0
              </span>
            </div>
            <p className="text-[11px] text-zinc-400 hidden sm:block">
              Cultural Intelligence Agent • Powered by Qloo Taste Graph
            </p>
          </div>
        </div>

        {/* View Switcher Tabs */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-zinc-900/90 border border-zinc-800">
          <button
            onClick={() => onViewChange("agent")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeView === "agent"
                ? "bg-cyber-cyan text-black shadow-neon-cyan"
                : "text-zinc-400 hover:text-white hover:bg-zinc-800/60"
            }`}
          >
            <Terminal className="w-3.5 h-3.5" />
            <span>Agent Scout</span>
          </button>
          <button
            onClick={() => hasLootDrop && onViewChange("dashboard")}
            disabled={!hasLootDrop}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeView === "dashboard"
                ? "bg-purple-600 text-white shadow-neon-purple"
                : hasLootDrop
                ? "text-zinc-400 hover:text-white hover:bg-zinc-800/60"
                : "text-zinc-600 cursor-not-allowed opacity-60"
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Loot Drop Split</span>
            {hasLootDrop && (
              <span className="w-2 h-2 rounded-full bg-cyber-cyan animate-ping" />
            )}
          </button>
        </div>

        {/* Status Pill & External Links */}
        <div className="flex items-center gap-3">
          {/* Health Status Indicator */}
          <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900 border border-zinc-800 text-xs">
            <span
              className={`w-2 h-2 rounded-full ${
                health.qloo_connected
                  ? "bg-emerald-400 shadow-[0_0_8px_#34d399]"
                  : "bg-amber-400 animate-pulse"
              }`}
            />
            <span className="text-zinc-300 font-mono text-[11px]">
              {health.qloo_connected
                ? `Qloo API: Connected (${health.qloo_latency_ms || 45}ms)`
                : "Qloo API: Connecting..."}
            </span>
          </div>

          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition-colors"
            title="View Source on GitHub"
          >
            <Github className="w-4 h-4" />
          </a>
        </div>
      </div>
    </header>
  );
};
