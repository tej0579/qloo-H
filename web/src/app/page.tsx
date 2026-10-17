"use client";

import React, { useState, useEffect, useRef } from "react";

interface CounterPrompt {
  question: string;
  options: string[];
}

interface ChatMessage {
  id: string;
  sender: "user" | "bot";
  text: string;
  turn?: number;
  status?: string;
  is_rollback?: boolean;
  counter_prompt?: CounterPrompt;
  qloo_data?: Record<string, any>;
  final_synthesis?: Record<string, any>;
  timestamp: string;
}

const API_BASE = "http://127.0.0.1:8000";

const QUICK_ANCHORS = [
  "Elden Ring",
  "Cyberpunk 2077",
  "Hades",
  "DOOM",
  "Persona 5"
];

const TURN_STEPS = [
  { turn: 0, label: "Turn 0: Awaiting Game" },
  { turn: 1, label: "Turn 1: Mechanics Calibration" },
  { turn: 2, label: "Turn 2: Aesthetics Calibration" },
  { turn: 3, label: "Turn 3: Platform Scoping" },
  { turn: 4, label: "Turn 4: Final Synthesis" }
];

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      sender: "bot",
      text: "### 👋 Welcome to Qloo Videogame Cultural Intelligence Agent\n\nI specialize strictly in `urn:entity:videogame`. I do not guess using generic LLM clichés.\n\nGive me a video game you love (e.g. **Elden Ring**, **Cyberpunk 2077**, **Hades**), and I will query Qloo's 250M+ entity taste graph, calibrate your mechanics and aesthetic preferences through **3 targeted counter-prompts**, and synthesize mathematically validated recommendations.",
      turn: 0,
      timestamp: "Just now",
    },
  ]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(`sess_${Date.now()}`);
  const [currentTurn, setCurrentTurn] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  const [qlooConnected, setQlooConnected] = useState(true);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/health`)
      .then((res) => res.json())
      .then((data) => setQlooConnected(Boolean(data.qloo_connected)))
      .catch(() => setQlooConnected(false));
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async (textToSend?: string) => {
    const query = (textToSend || input).trim();
    if (!query || loading) return;

    const userMsg: ChatMessage = {
      id: `user_${Date.now()}`,
      sender: "user",
      text: query,
      timestamp: "Now",
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, message: query }),
      });

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const data = await res.json();

      const botMsg: ChatMessage = {
        id: `bot_${Date.now()}`,
        sender: "bot",
        text: data.message,
        turn: data.turn,
        status: data.status,
        is_rollback: data.is_rollback,
        counter_prompt: data.counter_prompt,
        qloo_data: data.qloo_data,
        final_synthesis: data.final_synthesis,
        timestamp: "Now",
      };

      setMessages((prev) => [...prev, botMsg]);
      setCurrentTurn(data.turn);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: `err_${Date.now()}`,
          sender: "bot",
          text: `⚠️ **Connection Error**: Could not reach backend server at ${API_BASE}. Make sure the FastAPI backend is running.`,
          is_rollback: true,
          timestamp: "Now",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    try {
      await fetch(`${API_BASE}/api/reset`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId }),
      });
    } catch {}

    const newSessionId = `sess_${Date.now()}`;
    setSessionId(newSessionId);
    setCurrentTurn(0);
    setMessages([
      {
        id: `welcome_${Date.now()}`,
        sender: "bot",
        text: "Session cleared. What video game or franchise would you like to scout next?",
        turn: 0,
        timestamp: "Just now",
      },
    ]);
  };

  return (
    <div className="flex flex-col h-screen max-w-5xl mx-auto px-3 sm:px-6 py-4">
      {/* Top Console Bar */}
      <header className="rounded-2xl bg-[#0d0f18] border border-zinc-800 p-4 mb-3 shadow-xl flex flex-wrap items-center justify-between gap-3 shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 text-xl font-bold shadow-[0_0_15px_rgba(0,240,255,0.15)]">
            🎮
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm tracking-wide text-white">
                QLOO VIDEOGAME CULTURAL AGENT
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30 font-semibold">
                Category 1/14: urn:entity:videogame
              </span>
            </div>
            <p className="text-[11px] text-zinc-400 font-mono">
              Loop: Ingest &rarr; Qloo Search &rarr; Counter-Prompts &rarr; Accumulate &rarr; Final LLM
            </p>
          </div>
        </div>

        {/* State Badge & Actions */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-zinc-900 border border-zinc-700/80 text-xs font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-zinc-400">State:</span>
            <span className="text-cyan-400 font-bold">
              {TURN_STEPS[currentTurn]?.label || `Turn ${currentTurn}`}
            </span>
          </div>

          <button
            onClick={handleReset}
            className="px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white transition-colors border border-zinc-700"
          >
            Reset Loop
          </button>
        </div>
      </header>

      {/* Turn Progress Steps Indicator */}
      <div className="grid grid-cols-5 gap-1.5 mb-3 shrink-0">
        {TURN_STEPS.map((step) => {
          const isActive = currentTurn === step.turn;
          const isDone = currentTurn > step.turn;
          return (
            <div
              key={step.turn}
              className={`p-2 rounded-lg text-center font-mono text-[11px] border transition-all ${
                isActive
                  ? "bg-cyan-950/40 border-cyan-500/60 text-cyan-300 shadow-[0_0_10px_rgba(0,240,255,0.15)] font-bold"
                  : isDone
                  ? "bg-zinc-900/60 border-zinc-800 text-emerald-400 font-medium"
                  : "bg-zinc-900/30 border-zinc-800/60 text-zinc-600"
              }`}
            >
              <div className="text-[9px] uppercase tracking-wider">Step {step.turn}</div>
              <div className="truncate">
                {step.turn === 0 && "Anchor"}
                {step.turn === 1 && "Mechanics"}
                {step.turn === 2 && "Aesthetic"}
                {step.turn === 3 && "Platform"}
                {step.turn === 4 && "Synthesis"}
              </div>
            </div>
          );
        })}
      </div>

      {/* Chat Messages Log */}
      <main className="flex-1 overflow-y-auto rounded-2xl bg-[#0d0f18]/90 border border-zinc-800/80 p-4 sm:p-6 space-y-4 shadow-xl custom-scrollbar">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex flex-col ${
              msg.sender === "user" ? "items-end" : "items-start"
            }`}
          >
            {/* Sender Label */}
            <div className="flex items-center gap-1.5 text-[10px] text-zinc-500 font-mono mb-1 px-1">
              <span>{msg.sender === "user" ? "You" : "Qloo Agent"}</span>
            </div>

            {/* User Message Bubble */}
            {msg.sender === "user" ? (
              <div className="max-w-md sm:max-w-lg px-4 py-2.5 rounded-2xl rounded-tr-sm bg-gradient-to-r from-cyan-500 to-blue-600 text-black font-semibold text-sm shadow-[0_0_15px_rgba(0,240,255,0.2)]">
                {msg.text}
              </div>
            ) : (
              /* Bot Message Container */
              <div className="max-w-xl sm:max-w-2xl space-y-3">
                {/* Rollback Intercept Banner */}
                {msg.is_rollback && (
                  <div className="p-3.5 rounded-xl bg-red-950/40 border border-red-500/50 text-xs text-red-200 flex items-start gap-2.5 shadow-lg">
                    <span className="text-base shrink-0">⚠️</span>
                    <div className="leading-relaxed">{msg.text}</div>
                  </div>
                )}

                {/* Normal Bot Message */}
                {!msg.is_rollback && (
                  <div className="p-4 rounded-2xl rounded-tl-sm bg-[#121524] border border-zinc-800/90 text-sm text-zinc-200 leading-relaxed space-y-3 shadow-md">
                    {/* Qloo Ingested Entity Pill */}
                    {msg.qloo_data && msg.qloo_data.anchor && (
                      <div className="p-2.5 rounded-lg bg-black/40 border border-cyan-500/30 text-xs font-mono space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="text-cyan-400 font-bold flex items-center gap-1">
                            ✓ Qloo Ingestion:
                          </span>
                          <span className="text-white font-bold">{msg.qloo_data.anchor.name}</span>
                          {msg.qloo_data.anchor.id && (
                            <span className="text-zinc-500 text-[10px]">
                              (UUID: {String(msg.qloo_data.anchor.id).substring(0, 8)}...)
                            </span>
                          )}
                        </div>
                        {msg.qloo_data.anchor.tags && (
                          <div className="flex flex-wrap gap-1 pt-1">
                            {msg.qloo_data.anchor.tags.map((tag: string, idx: number) => (
                              <span
                                key={idx}
                                className="px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-300 text-[10px]"
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Bot Text Content */}
                    <div className="whitespace-pre-wrap">{msg.text}</div>

                    {/* Counter Prompt Options Chips */}
                    {msg.counter_prompt && msg.counter_prompt.options?.length > 0 && (
                      <div className="pt-2 border-t border-zinc-800/90 space-y-2">
                        <div className="text-[11px] text-zinc-400 font-mono flex items-center gap-1">
                          <span className="text-purple-400">✨</span>
                          <span>Select an option to calibrate or type your custom answer:</span>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {msg.counter_prompt.options.map((option, idx) => (
                            <button
                              key={idx}
                              onClick={() => handleSend(option)}
                              disabled={loading}
                              className="px-3 py-1.5 rounded-lg bg-zinc-800/90 hover:bg-cyan-500/20 hover:border-cyan-400 hover:text-white border border-zinc-700 text-xs text-zinc-300 font-medium transition-all text-left flex items-center gap-1.5 group cursor-pointer"
                            >
                              <span className="text-cyan-400 group-hover:translate-x-0.5 transition-transform">
                                &rarr;
                              </span>
                              <span>{option}</span>
                            </button>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Final Synthesis Presentation */}
                    {msg.final_synthesis && msg.final_synthesis.candidates && (
                      <div className="space-y-3 pt-3 border-t border-zinc-800">
                        <div className="text-xs uppercase font-mono font-bold text-cyan-400 tracking-wider flex items-center gap-1.5">
                          <span>🎯</span>
                          <span>Correlated Qloo Matches:</span>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                          {msg.final_synthesis.candidates.map((c: any, cidx: number) => (
                            <div
                              key={cidx}
                              className="p-3 rounded-xl bg-black/60 border border-cyan-500/30 space-y-1.5 shadow-[0_0_12px_rgba(0,240,255,0.08)]"
                            >
                              <div className="flex items-center justify-between">
                                <span className="font-bold text-xs text-white truncate">
                                  {c.name}
                                </span>
                                <span className="text-[10px] font-mono font-bold text-emerald-400 px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-500/30">
                                  {Math.round(c.score || 90)}% Affinity
                                </span>
                              </div>
                              <div className="flex flex-wrap gap-1">
                                {(c.tags || []).slice(0, 2).map((t: string, tidx: number) => (
                                  <span
                                    key={tidx}
                                    className="text-[9px] px-1 py-0.5 rounded bg-zinc-800 text-zinc-400"
                                  >
                                    {t}
                                  </span>
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {/* Loading Spinner */}
        {loading && (
          <div className="flex items-center gap-2 text-xs font-mono text-cyan-400 animate-pulse pl-1">
            <span className="animate-spin text-sm">⚙️</span>
            <span>Qloo Graph Engine reasoning &amp; calculating affinities...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </main>

      {/* Quick Anchor Bar (Turn 0) */}
      {currentTurn === 0 && (
        <div className="px-4 py-2 border-t border-zinc-800/80 bg-[#0d0f18]/60 flex flex-wrap items-center gap-1.5 shrink-0 rounded-t-xl mt-2">
          <span className="text-[11px] font-mono text-zinc-500 flex items-center gap-1 mr-1">
            <span className="text-purple-400">⚡</span>
            Popular Anchors:
          </span>
          {QUICK_ANCHORS.map((anchor, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(anchor)}
              disabled={loading}
              className="px-2.5 py-1 rounded-md text-xs font-medium bg-zinc-900 border border-zinc-700/80 hover:border-cyan-400 hover:text-white text-zinc-300 transition-colors cursor-pointer"
            >
              + {anchor}
            </button>
          ))}
        </div>
      )}

      {/* Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="p-3 border-t border-zinc-800 bg-[#0d0f18] flex items-center gap-2 shrink-0 rounded-b-2xl shadow-xl"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={
            currentTurn === 0
              ? "Enter a video game title (e.g. Elden Ring, Hades, Cyberpunk 2077)..."
              : "Type your answer or select one of the counter-prompt options above..."
          }
          disabled={loading}
          className="flex-1 px-4 py-2.5 rounded-xl bg-zinc-900/90 border border-zinc-700 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 transition-all font-sans"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="px-5 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 text-black font-bold text-sm transition-all shadow-[0_0_15px_rgba(0,240,255,0.3)] cursor-pointer"
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </form>
    </div>
  );
}
