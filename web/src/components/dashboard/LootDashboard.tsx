"use client";

import React, { useState } from "react";
import { LootDropPayload } from "@/types/loot";
import { ComparatorSplit } from "./ComparatorSplit";
import { AffinityRadar } from "./AffinityRadar";
import { CategorySection } from "./CategorySection";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Share2,
  Download,
  RotateCcw,
  Sparkles,
  MapPin,
  CheckCircle,
  Database,
  Gamepad2,
  Compass,
  ChevronDown,
  ChevronUp,
  Clock3,
  Route,
} from "lucide-react";

interface LootDashboardProps {
  payload: LootDropPayload;
  onReset: () => void;
}

export const LootDashboard: React.FC<LootDashboardProps> = ({ payload, onReset }) => {
  const [copied, setCopied] = useState(false);
  const [questExpanded, setQuestExpanded] = useState(false);

  const handleShare = () => {
    const text = `🎮 IRL Loot Drop for ${payload.seed_games.map((g) => g.name).join(" + ")}:\nPersona: ${payload.persona_title}\nTerritory: ${payload.location}\nPowered by Qloo Taste Intelligence.`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadJson = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(payload, null, 2));
    const downloadAnchor = document.createElement("a");
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `irl-lootdrop-${payload.session_id}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="max-w-7xl mx-auto space-y-10 py-6 animate-in fade-in duration-300">
      {/* Persona Header Card */}
      <div className="relative rounded-3xl bg-cyber-card/90 border border-cyber-cyan/40 p-6 sm:p-10 shadow-neon-cyan/15 overflow-hidden">
        {/* Neon Glow Accents */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-cyber-cyan/15 via-purple-600/10 to-transparent rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="space-y-3 max-w-3xl">
            {/* Meta Tags */}
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-cyber-cyan/15 text-cyber-cyan border border-cyber-cyan/40 uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5" />
                Synthesized Persona
              </span>
              <span
                className={`px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold border uppercase tracking-wider flex items-center gap-1.5 ${
                  payload.data_source === "qloo_live"
                    ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/40"
                    : "bg-amber-500/10 text-amber-300 border-amber-500/40"
                }`}
              >
                {payload.data_source === "qloo_live" ? (
                  <CheckCircle className="w-3.5 h-3.5" />
                ) : (
                  <Database className="w-3.5 h-3.5" />
                )}
                {payload.data_source === "qloo_live" ? "Qloo Live Verified" : "Offline Demo Fallback"}
              </span>
              {payload.location && (
                <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono bg-zinc-800 text-zinc-300 border border-zinc-700 flex items-center gap-1">
                  <MapPin className="w-3 h-3 text-emerald-400" />
                  {payload.location}
                </span>
              )}
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono bg-zinc-800 text-zinc-400 border border-zinc-700 flex items-center gap-1">
                <Gamepad2 className="w-3 h-3 text-purple-400" />
                {payload.seed_games.map((g) => g.name).join(" • ")}
              </span>
            </div>

            {/* Persona Title */}
            <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-zinc-100">
              {payload.persona_title}
            </h1>

            {/* Persona Description */}
            <p className="text-sm sm:text-base text-zinc-300 leading-relaxed">
              {payload.persona_description}
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap sm:flex-col gap-2 shrink-0">
            <Button
              onClick={handleShare}
              variant="outline"
              size="sm"
              className="flex items-center gap-2"
            >
              <Share2 className="w-3.5 h-3.5" />
              <span>{copied ? "Copied Link!" : "Share Loot"}</span>
            </Button>
            <Button
              onClick={handleDownloadJson}
              variant="secondary"
              size="sm"
              className="flex items-center gap-2"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export JSON</span>
            </Button>
            <Button
              onClick={onReset}
              variant="ghost"
              size="sm"
              className="flex items-center gap-2 text-zinc-400 hover:text-white"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>New Drop</span>
            </Button>
          </div>
        </div>

        {/* Quick Stats Bar */}
        <div className="relative z-10 grid grid-cols-2 sm:grid-cols-4 gap-4 pt-8 mt-8 border-t border-zinc-800/80 text-xs">
          <div>
            <div className="text-zinc-500 font-mono text-[11px] uppercase">Seed Games</div>
            <div className="text-sm font-bold text-zinc-200 mt-0.5">{payload.seed_games.length} Anchors</div>
          </div>
          <div>
            <div className="text-zinc-500 font-mono text-[11px] uppercase">Grounded Items</div>
            <div className="text-sm font-bold text-cyber-cyan mt-0.5">
              {payload.categories.reduce((acc, c) => acc + c.items.length, 0)} Entities
            </div>
          </div>
          <div>
            <div className="text-zinc-500 font-mono text-[11px] uppercase">Overall Match Score</div>
            <div className="text-sm font-bold text-emerald-400 mt-0.5">
              {payload.overall_match_score == null
                ? "N/A"
                : `${Math.round(payload.overall_match_score)}% average affinity`}
            </div>
          </div>
          <div>
            <div className="text-zinc-500 font-mono text-[11px] uppercase">Recommendation Source</div>
            <div className={`text-sm font-bold mt-0.5 flex items-center gap-1 ${
              payload.data_source === "qloo_live" ? "text-emerald-400" : "text-amber-300"
            }`}>
              {payload.data_source === "qloo_live" ? "Live Qloo insights" : "Offline demo data"}
            </div>
          </div>
        </div>
      </div>

      {/* 🏆 Feature #1: Split-Screen Comparator (Judging Centerpiece) */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-cyber-cyan shadow-[0_0_10px_#00f0ff]" />
          <h2 className="text-xl font-bold tracking-tight text-zinc-100">
            Split-Screen Taste Comparator
          </h2>
        </div>
        <ComparatorSplit
          comparator={payload.comparator}
          dataSource={payload.data_source}
          archetypeTitle={payload.archetype_title || payload.persona_title}
        />
      </section>

      <section className="rounded-2xl border border-amber-400/30 bg-gradient-to-br from-amber-950/30 via-zinc-900/90 to-cyber-card/90 shadow-[0_0_24px_rgba(251,191,36,0.08)] overflow-hidden">
        <button
          type="button"
          aria-expanded={questExpanded}
          onClick={() => setQuestExpanded((expanded) => !expanded)}
          className="w-full flex items-center justify-between gap-4 p-5 sm:p-6 text-left hover:bg-amber-400/5 transition-colors"
        >
          <span className="flex items-center gap-3">
            <span className="rounded-xl bg-amber-400/10 border border-amber-300/30 p-2.5 text-amber-300">
              <Route className="w-5 h-5" />
            </span>
            <span>
              <span className="block text-lg font-black text-zinc-100">⚡ IRL Saturday Quest Log</span>
              <span className="block mt-1 text-xs text-zinc-400">A four-step day woven from your recommendations in {payload.location || "your city"}.</span>
            </span>
          </span>
          {questExpanded ? <ChevronUp className="w-5 h-5 text-amber-300 shrink-0" /> : <ChevronDown className="w-5 h-5 text-amber-300 shrink-0" />}
        </button>

        {questExpanded && (
          <div className="px-5 pb-6 sm:px-6">
            {payload.quest_log?.length ? (
              <ol className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {payload.quest_log.map((step, index) => (
                  <li key={`${step.time}-${step.title}`} className="relative rounded-xl border border-zinc-700/80 bg-zinc-950/70 p-4">
                    <div className="flex items-center gap-2 text-[11px] font-mono uppercase tracking-wider text-amber-300">
                      <Clock3 className="w-3.5 h-3.5" />
                      <span>{step.time}</span>
                      <span className="text-zinc-600">/</span>
                      <span className="text-zinc-300">Step {index + 1}</span>
                    </div>
                    <h3 className="mt-2 text-sm font-bold text-zinc-100">{step.title}</h3>
                    <div className="mt-1 text-base font-black text-cyber-cyan">{step.recommendation}</div>
                    <p className="mt-2 text-xs leading-relaxed text-zinc-400">{step.description}</p>
                  </li>
                ))}
              </ol>
            ) : (
              <p className="rounded-xl border border-zinc-700 bg-zinc-950/70 p-4 text-sm text-zinc-400">
                This saved drop predates the quest log. Generate a new drop to build its four-step itinerary.
              </p>
            )}
          </div>
        )}
      </section>

      {/* Visualizer & Persona Radar Section */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <AffinityRadar metrics={payload.radar_metrics} />
        </div>

        {/* Aesthetic Field Notes Card */}
        <div className="rounded-2xl bg-cyber-card/80 border border-zinc-800 p-5 space-y-4 flex flex-col justify-between">
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <Compass className="w-4 h-4 text-purple-400" />
              <h3 className="text-sm font-bold text-zinc-100">
                Taste Engineering Notes
              </h3>
            </div>
            <p className="text-xs text-zinc-400 leading-relaxed">
              Standard LLM models operate on surface-level text tokens—when asked about games like{" "}
              <strong className="text-zinc-200">
                {payload.seed_games.map((g) => g.name).join(" or ")}
              </strong>
              , they default to gamer-branded merchandise or direct videogame soundtrack loops.
            </p>
            <p className="text-xs text-zinc-400 leading-relaxed">
              By evaluating multi-dimensional co-occurrences through Qloo's affinity graph, we bridge
              the player's emotional immersion to authentic fashion houses, sound design, and local spaces.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-zinc-900 border border-zinc-800 text-[11px] text-zinc-300 font-mono space-y-1">
            <div className="text-cyber-cyan font-bold">API Route Signature:</div>
            <div>POST /api/chat {"->"} action: EXECUTE</div>
            <div>filter.type: brand, artist, place, movie</div>
          </div>
        </div>
      </section>

      {/* Category Breakdown (Streetwear, Soundtracks, Venues, Cinema) */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-purple-500 shadow-[0_0_10px_#9d4edd]" />
          <h2 className="text-xl font-bold tracking-tight text-zinc-100">
            Synthesized Real-World Loot Drop
          </h2>
        </div>
        <CategorySection categories={payload.categories} />
      </section>
    </div>
  );
};
