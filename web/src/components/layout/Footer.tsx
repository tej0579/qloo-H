import React from "react";
import { Terminal, Shield, Award } from "lucide-react";

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-cyber-border/80 bg-cyber-dark/60 py-8 px-4 sm:px-6 lg:px-8 mt-16 text-xs text-zinc-500">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-2 h-2 rounded-full bg-cyber-cyan shadow-[0_0_8px_#00f0ff]" />
          <span>
            Built for <strong className="text-zinc-300">Qloo Taste AI Hackathon 2026</strong> • Open-Source MIT License
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-4 text-zinc-400">
          <span className="flex items-center gap-1">
            <Terminal className="w-3.5 h-3.5 text-cyber-cyan" />
            <span>FastAPI + Next.js 14</span>
          </span>
          <span>•</span>
          <span className="flex items-center gap-1">
            <Shield className="w-3.5 h-3.5 text-purple-400" />
            <span>URN Ontology: brand, artist, place, videogame</span>
          </span>
          <span>•</span>
          <span className="flex items-center gap-1">
            <Award className="w-3.5 h-3.5 text-emerald-400" />
            <span>Grounded Taste Intelligence</span>
          </span>
        </div>
      </div>
    </footer>
  );
};
