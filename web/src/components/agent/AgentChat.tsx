"use client";

import React, { useState } from "react";
import { UserGameSelection, ClarificationAnswer } from "@/types/agent";
import { LootDropPayload } from "@/types/loot";
import { GameSearchInput } from "./GameSearchInput";
import { ClarificationStep } from "./ClarificationStep";
import { sendChatAction } from "@/lib/api";
import { Terminal, Sparkles, ArrowRight, ShieldCheck, Zap, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";

interface AgentChatProps {
  onLootDropReady: (payload: LootDropPayload) => void;
}

export const AgentChat: React.FC<AgentChatProps> = ({ onLootDropReady }) => {
  const [selectedGames, setSelectedGames] = useState<UserGameSelection[]>([
    {
      id: "BAF6317A-DF94-4C90-92AE-63F86560C21B",
      name: "Elden Ring",
      types: ["urn:entity:videogame"],
    },
  ]);
  const [step, setStep] = useState<"SELECT_GAMES" | "CLARIFICATION" | "SYNTHESIZING">("SELECT_GAMES");
  const [clarificationQuestions, setClarificationQuestions] = useState<any[]>([]);
  const [agentLog, setAgentLog] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSelectGame = (game: UserGameSelection) => {
    setSelectedGames((prev) => [...prev, game]);
  };

  const handleRemoveGame = (id: string) => {
    setSelectedGames((prev) => prev.filter((g) => g.id !== id && g.name !== id));
  };

  // Step 1 -> Step 2: Lock in games and fetch clarification questions
  const handleProceedToClarification = async () => {
    if (selectedGames.length === 0) return;
    setLoading(true);
    setAgentLog((prev) => [...prev, `[SEED] Verified ${selectedGames.length} game entity UUIDs in Qloo graph...`]);

    try {
      const res = await sendChatAction({
        action: "SEED_GAMES",
        games: selectedGames,
      });

      if (res.clarification_questions) {
        setClarificationQuestions(res.clarification_questions);
        setStep("CLARIFICATION");
        setAgentLog((prev) => [
          ...prev,
          `[INTERCEPT] Halting agent execution for 2 spatial & aesthetic clarification questions.`,
        ]);
      }
    } catch (err: any) {
      console.error("Agent error:", err);
      // Fallback
      setStep("CLARIFICATION");
    } finally {
      setLoading(false);
    }
  };

  // Step 2 -> Step 3: Execute Qloo pipeline + Naked LLM comparator
  const handleExecute = async (answers: ClarificationAnswer) => {
    setStep("SYNTHESIZING");
    setLoading(true);
    setAgentLog((prev) => [
      ...prev,
      `[SCOUT] Target City: ${answers.location} | Aesthetic: ${answers.aesthetic_focus}`,
      `[GRAPH] Dispatching parallel /v2/insights for brand, artist, place, and movie...`,
      `[BASELINE] Generating naked LLM benchmark without taste graph tools...`,
    ]);

    try {
      const res = await sendChatAction({
        action: "EXECUTE",
        games: selectedGames,
        clarification: answers,
      });

      if (res.lootdrop) {
        setAgentLog((prev) => [...prev, `[COMPLETE] IRL Loot Drop synthesized with grounded affinity scores!`]);
        setTimeout(() => {
          onLootDropReady(res.lootdrop!);
        }, 600);
      }
    } catch (err) {
      console.error("Execution error:", err);
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedGames([]);
    setStep("SELECT_GAMES");
    setAgentLog([]);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      {/* Hero Title & Mission */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyber-card border border-cyber-cyan/30 text-cyber-cyan text-xs font-mono">
          <Zap className="w-3.5 h-3.5" />
          <span>Cultural Intelligence vs. Generic LLM Clichés</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-zinc-100">
          Turn Your Games Into An{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyber-cyan via-purple-400 to-pink-500">
            IRL Lifestyle Drop
          </span>
        </h1>
        <p className="text-sm sm:text-base text-zinc-400 max-w-2xl mx-auto">
          Standard chat models guess with graphic tees and energy drinks. Qloo’s taste graph maps
          what players <strong className="text-zinc-200">actually wear, listen to, and inhabit</strong>.
        </p>
      </div>

      {/* Main Console Box */}
      <div className="rounded-2xl bg-cyber-card/80 backdrop-blur-xl border border-cyber-border shadow-2xl p-6 sm:p-8 space-y-6">
        {/* Terminal Header */}
        <div className="flex items-center justify-between pb-4 border-b border-zinc-800">
          <div className="flex items-center gap-2 text-xs font-mono text-zinc-400">
            <Terminal className="w-4 h-4 text-cyber-cyan" />
            <span>agent_orchestrator.py • mode: cultural_scout</span>
          </div>
          {selectedGames.length > 0 && (
            <button
              onClick={handleReset}
              className="text-xs text-zinc-500 hover:text-zinc-300 flex items-center gap-1 transition-colors"
            >
              <RotateCcw className="w-3 h-3" />
              <span>Reset</span>
            </button>
          )}
        </div>

        {/* Step 1: Input Games */}
        {step === "SELECT_GAMES" && (
          <div className="space-y-6 animate-in fade-in duration-200">
            <div className="space-y-1">
              <h2 className="text-base font-bold text-zinc-100 flex items-center gap-2">
                <span>Select 1 to 3 Anchor Video Games</span>
                <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/30">
                  Step 1 of 2
                </span>
              </h2>
              <p className="text-xs text-zinc-400">
                Type any game in the catalog or choose from the quick seeds below.
              </p>
            </div>

            <GameSearchInput
              selectedGames={selectedGames}
              onSelectGame={handleSelectGame}
              onRemoveGame={handleRemoveGame}
              onProceed={handleProceedToClarification}
              disabled={loading}
            />

            {selectedGames.length > 0 && (
              <div className="pt-2 flex justify-end">
                <Button
                  onClick={handleProceedToClarification}
                  variant="primary"
                  size="lg"
                  loading={loading}
                  className="flex items-center gap-2"
                >
                  <span>Lock In Seeds &amp; Continue</span>
                  <ArrowRight className="w-4 h-4" />
                </Button>
              </div>
            )}
          </div>
        )}

        {/* Step 2: Clarification Questions */}
        {step === "CLARIFICATION" && (
          <ClarificationStep
            questions={clarificationQuestions}
            onSubmit={handleExecute}
            loading={loading}
          />
        )}

        {/* Step 3: Synthesizing Loader */}
        {step === "SYNTHESIZING" && (
          <div className="py-12 text-center space-y-6 animate-in fade-in duration-300">
            <div className="relative w-16 h-16 mx-auto flex items-center justify-center">
              <div className="absolute inset-0 rounded-full border-2 border-cyber-cyan/20 animate-ping" />
              <div className="absolute inset-0 rounded-full border-2 border-t-cyber-cyan border-r-purple-500 border-b-transparent border-l-transparent animate-spin" />
              <Sparkles className="w-7 h-7 text-cyber-cyan animate-pulse" />
            </div>

            <div className="space-y-2">
              <h3 className="text-lg font-bold text-zinc-100">
                Scouting Real-World Taste Graph...
              </h3>
              <p className="text-xs text-zinc-400 max-w-md mx-auto">
                Comparing unassisted LLM clichés against Qloo statistical co-occurrences across
                fashion, soundtracks, and physical venues.
              </p>
            </div>

            {/* Live Terminal Log */}
            <div className="max-w-lg mx-auto p-4 rounded-xl bg-black/60 border border-zinc-800 text-left font-mono text-[11px] space-y-1.5 text-zinc-400">
              {agentLog.map((log, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <span className="text-cyber-cyan">&gt;</span>
                  <span>{log}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Feature Highlights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
        <div className="p-4 rounded-xl bg-zinc-900/60 border border-zinc-800/80 space-y-2">
          <div className="text-cyber-cyan font-bold text-xs uppercase tracking-wider flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4" />
            No Hallucinated Venues
          </div>
          <p className="text-xs text-zinc-400">
            Every dining spot and listening bar is grounded in Qloo’s geographic database with verified addresses.
          </p>
        </div>

        <div className="p-4 rounded-xl bg-zinc-900/60 border border-zinc-800/80 space-y-2">
          <div className="text-purple-400 font-bold text-xs uppercase tracking-wider flex items-center gap-1.5">
            <Sparkles className="w-4 h-4" />
            Cross-Domain Affinities
          </div>
          <p className="text-xs text-zinc-400">
            Connects video games directly to apparel brands, indie music acts, and auteur cinema.
          </p>
        </div>

        <div className="p-4 rounded-xl bg-zinc-900/60 border border-zinc-800/80 space-y-2">
          <div className="text-emerald-400 font-bold text-xs uppercase tracking-wider flex items-center gap-1.5">
            <Terminal className="w-4 h-4" />
            Split-Screen Comparator
          </div>
          <p className="text-xs text-zinc-400">
            See the side-by-side contrast between lazy LLM clichés and real subcultural reality.
          </p>
        </div>
      </div>
    </div>
  );
};
