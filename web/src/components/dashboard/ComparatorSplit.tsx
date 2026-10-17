import React from "react";
import { ComparatorPayload } from "@/types/loot";
import { AlertTriangle, CheckCircle2, Sparkles, Flame, ShieldAlert, Cpu } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface ComparatorSplitProps {
  comparator: ComparatorPayload;
  dataSource: "qloo_live" | "demo_fallback";
  archetypeTitle?: string;
}

export const ComparatorSplit: React.FC<ComparatorSplitProps> = ({ comparator, dataSource, archetypeTitle }) => {
  const hasLiveQlooData = dataSource === "qloo_live";
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-4 rounded-xl bg-gradient-to-r from-red-950/20 via-zinc-900 to-cyber-cyan/10 border border-zinc-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-zinc-800 text-cyber-cyan">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-zinc-100 flex items-center gap-2">
              <span>The Split-Screen Taste Comparator</span>
              <span className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded border ${
                hasLiveQlooData
                  ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
                  : "bg-amber-500/20 text-amber-300 border-amber-500/30"
              }`}>
                {hasLiveQlooData ? "Live Contrast" : "Offline Demo Contrast"}
              </span>
            </h3>
            <p className="text-xs text-zinc-400">
              {hasLiveQlooData
                ? "Comparing generic LLM guesses with recommendations returned by Qloo's cultural graph."
                : "Comparing generic LLM guesses with illustrative offline demo recommendations."}
            </p>
          </div>
        </div>

        <div className="text-right">
          <div className="text-[11px] font-mono text-zinc-400">
            Hackathon Benchmark
          </div>
          <div className={`text-xs font-semibold ${hasLiveQlooData ? "text-cyber-cyan" : "text-amber-300"}`}>
            {hasLiveQlooData ? "Live Qloo Insights" : "Demo Data, Not Live Qloo"}
          </div>
        </div>
      </div>

      {/* Side-by-Side Dual Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Without Qloo / Standard LLM */}
        <div className="rounded-2xl bg-zinc-900/60 border border-red-500/30 p-5 space-y-4 relative overflow-hidden">
          <div className="absolute top-0 right-0 transform translate-x-4 -translate-y-4 w-28 h-28 bg-red-500/10 rounded-full blur-2xl pointer-events-none" />

          {/* Column Header */}
          <div className="flex items-center justify-between pb-3 border-b border-red-500/20">
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-red-400" />
              <span className="font-bold text-sm text-red-300">
                WITHOUT QLOO (Standard LLM Alone)
              </span>
            </div>
            <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-red-500/10 text-red-400 border border-red-500/30">
              Cliché Hallucination
            </span>
          </div>

          <p className="text-xs text-zinc-400 italic">
            LLMs lack consumer behavioral data—they guess based on literal game titles, cheap promotional merchandise, and shallow tropes.
          </p>

          {/* Cliché Items List */}
          <div className="space-y-3">
            {comparator.unassisted_llm_response.map((item, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-xl bg-zinc-950/60 border border-red-500/20 space-y-1.5"
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-zinc-200 flex items-center gap-1.5">
                    <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                    {item.item_name}
                  </span>
                  <span className="text-[10px] font-mono text-red-400 px-1.5 py-0.5 rounded bg-red-950/50 border border-red-800/60">
                    {item.vibe_or_tag}
                  </span>
                </div>
                <p className="text-[11px] text-zinc-400">
                  {item.detail}
                </p>
              </div>
            ))}
          </div>

          <div className="p-3 rounded-lg bg-red-950/20 border border-red-900/40 text-[11px] text-red-300">
            ❌ <strong>Result:</strong> Walking billboard merchandise, generic royalty-free stream audio, and suburban chain arcades.
          </div>
        </div>

        {/* Right Column: With Qloo / Taste Graph Reality */}
        <div className="rounded-2xl bg-cyber-card/90 border border-cyber-cyan/40 p-5 space-y-4 shadow-neon-cyan/15 relative overflow-hidden">
          <div className="absolute top-0 right-0 transform translate-x-4 -translate-y-4 w-32 h-32 bg-cyber-cyan/10 rounded-full blur-2xl pointer-events-none" />

          <div className="relative rounded-xl border border-purple-400/30 bg-purple-500/10 px-4 py-3">
            <div className="text-[10px] font-mono font-bold uppercase tracking-[0.18em] text-purple-300">
              IRL Character Class
            </div>
            <div className="mt-1 text-xl sm:text-2xl font-black tracking-tight text-white">
              {archetypeTitle || "Cultural Wayfarer"}
            </div>
          </div>

          {/* Column Header */}
          <div className="flex items-center justify-between pb-3 border-b border-cyber-cyan/30">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-cyber-cyan" />
              <span className="font-bold text-sm text-cyber-cyan">
                {hasLiveQlooData ? "WITH QLOO (Cultural Taste Graph)" : "OFFLINE DEMO RECOMMENDATIONS"}
              </span>
            </div>
            <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/40">
              {hasLiveQlooData ? "Qloo Live Results" : "Illustrative Fallback"}
            </span>
          </div>

          <p className="text-xs text-zinc-300">
            {hasLiveQlooData
              ? "Recommendations returned by Qloo's cross-domain taste graph for the selected game entities."
              : "These examples come from the local demo catalog and do not represent live Qloo results."}
          </p>

          {/* Validated Qloo Items List */}
          <div className="space-y-3">
            {comparator.qloo_grounded_response.map((item, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-xl bg-zinc-900/90 border border-cyber-cyan/30 space-y-1.5 shadow-[0_0_12px_rgba(0,240,255,0.08)]"
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-zinc-100 flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-cyber-cyan" />
                    {item.item_name}
                  </span>
                  <span className="text-[10px] font-mono text-emerald-400 px-1.5 py-0.5 rounded bg-emerald-950/50 border border-emerald-500/40 font-bold">
                    {item.score ? `${Math.round(item.score)}% Affinity` : "Verified Match"}
                  </span>
                </div>
                <p className="text-[11px] text-zinc-300">
                  {item.detail}
                </p>
              </div>
            ))}
          </div>

          <div className="p-3 rounded-lg bg-cyber-cyan/10 border border-cyber-cyan/30 text-[11px] text-cyber-cyan">
            ✅ <strong>{hasLiveQlooData ? "Qloo results:" : "Demo examples:"}</strong> Elevated avant-garde techwear, virtuoso instrumental sound design, and brutalist hi-fi listening lounges.
          </div>
        </div>
      </div>

      {/* Deep-Dive Dimension Comparison Table */}
      {comparator.comparisons && comparator.comparisons.length > 0 && (
        <div className="p-5 rounded-2xl bg-zinc-900/80 border border-zinc-800 space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-zinc-200">
            <Flame className="w-4 h-4 text-purple-400" />
            Cultural Dimension Breakdown
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {comparator.comparisons.map((comp, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl bg-zinc-950/80 border border-zinc-800/80 space-y-2.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-zinc-200">{comp.dimension}</span>
                  <Badge variant="purple" className="text-[10px]">
                    Analysis
                  </Badge>
                </div>

                <div className="space-y-1 text-xs">
                  <div className="flex items-start gap-1.5 text-zinc-400">
                    <span className="text-red-400 font-mono shrink-0">Standard LLM:</span>
                    <span>{comp.unassisted_llm_cliche}</span>
                  </div>
                  <div className="flex items-start gap-1.5 text-zinc-200 font-medium">
                    <span className="text-cyber-cyan font-mono shrink-0">
                      {hasLiveQlooData ? "Qloo Results:" : "Demo Examples:"}
                    </span>
                    <span>{comp.qloo_grounded_reality}</span>
                  </div>
                </div>

                <div className="pt-2 border-t border-zinc-800/60 text-[11px] text-zinc-400 italic">
                  💡 {comp.why_it_matters}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Summary Verdict Callout */}
      <div className="p-4 rounded-xl bg-purple-950/20 border border-purple-500/30 text-xs text-purple-200 flex items-start gap-3">
        <Sparkles className="w-5 h-5 text-purple-400 shrink-0 mt-0.5" />
        <div>
          <strong className="text-white">Why This Wins:</strong> {comparator.summary_verdict}
        </div>
      </div>
    </div>
  );
};
