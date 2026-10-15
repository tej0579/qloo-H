"use client";

import React, { useState } from "react";
import { ClarificationQuestion, ClarificationAnswer } from "@/types/agent";
import { MapPin, Sparkles, Check, ArrowRight, Compass } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ClarificationStepProps {
  questions: ClarificationQuestion[];
  onSubmit: (answers: ClarificationAnswer) => void;
  loading?: boolean;
}

const CITY_PRESETS = [
  "Tokyo, Japan",
  "Austin, TX",
  "New York, NY",
  "London, UK",
  "Berlin, Germany",
  "Seoul, South Korea",
  "Seattle, WA",
  "Global / Online",
];

const AESTHETIC_PRESETS = [
  {
    id: "streetwear_audio",
    title: "Streetwear & Audio Setup",
    desc: "Tactical apparel, technical outerwear, and math-rock/industrial soundscapes",
    icon: "🧥",
  },
  {
    id: "cozy_dark_academia",
    title: "Cozy Hi-Fi & Dark Academia",
    desc: "Minimalist concrete cafes, pour-overs, vinyl listening, and atmospheric cinema",
    icon: "☕",
  },
  {
    id: "nightlife_dining",
    title: "Nightlife & Underground Bars",
    desc: "Dimly lit speakeasies, late-night ramen, craft spirits, and subcultural music",
    icon: "🍸",
  },
  {
    id: "full_immersion",
    title: "360° Full Loot Drop",
    desc: "Complete multi-category drop: apparel, audio, hangouts, and narrative cinema",
    icon: "⚡",
  },
];

export const ClarificationStep: React.FC<ClarificationStepProps> = ({
  questions,
  onSubmit,
  loading,
}) => {
  const [selectedCity, setSelectedCity] = useState("Tokyo, Japan");
  const [customCity, setCustomCity] = useState("");
  const [selectedAesthetic, setSelectedAesthetic] = useState("streetwear_audio");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const city = customCity.trim() || selectedCity;
    onSubmit({
      location: city,
      aesthetic_focus: selectedAesthetic,
    });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-6 rounded-2xl bg-cyber-card/90 border border-cyber-cyan/30 shadow-neon-cyan/10 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-300"
    >
      <div className="flex items-center gap-2.5 pb-3 border-b border-zinc-800">
        <Compass className="w-5 h-5 text-cyber-cyan" />
        <div>
          <h3 className="text-base font-bold text-zinc-100 flex items-center gap-2">
            <span>Agent Clarification Intercept</span>
            <span className="text-[11px] font-mono uppercase px-2 py-0.5 rounded bg-purple-500/20 text-purple-400 border border-purple-500/30">
              Step 2 of 2
            </span>
          </h3>
          <p className="text-xs text-zinc-400">
            Qloo needs 2 spatial &amp; aesthetic coordinates before dispatching the cultural graph.
          </p>
        </div>
      </div>

      {/* Question 1: Location */}
      <div className="space-y-3">
        <label className="text-xs font-semibold text-zinc-200 uppercase tracking-wider flex items-center gap-1.5">
          <MapPin className="w-3.5 h-3.5 text-cyber-cyan" />
          1. Which city or metro area should we scout for IRL hangouts and venues?
        </label>
        
        {/* Preset City Pills */}
        <div className="flex flex-wrap gap-2">
          {CITY_PRESETS.map((city) => (
            <button
              key={city}
              type="button"
              onClick={() => {
                setSelectedCity(city);
                setCustomCity("");
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                selectedCity === city && !customCity
                  ? "bg-cyber-cyan text-black font-bold shadow-neon-cyan"
                  : "bg-zinc-800/80 text-zinc-300 border border-zinc-700 hover:border-cyber-cyan/50 hover:text-white"
              }`}
            >
              {selectedCity === city && !customCity && <Check className="w-3 h-3" />}
              <span>{city}</span>
            </button>
          ))}
        </div>

        {/* Custom City Input */}
        <input
          type="text"
          value={customCity}
          onChange={(e) => setCustomCity(e.target.value)}
          placeholder="Or type another target city (e.g. Chicago, IL or Paris, France)..."
          className="w-full px-3.5 py-2 rounded-lg bg-zinc-900 border border-zinc-800 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-cyber-cyan"
        />
      </div>

      {/* Question 2: Aesthetic Upgrade Focus */}
      <div className="space-y-3">
        <label className="text-xs font-semibold text-zinc-200 uppercase tracking-wider flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-purple-400" />
          2. What area are you looking to upgrade first?
        </label>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {AESTHETIC_PRESETS.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => setSelectedAesthetic(item.id)}
              className={`p-3.5 rounded-xl text-left border transition-all relative overflow-hidden group ${
                selectedAesthetic === item.id
                  ? "bg-purple-950/30 border-purple-500 shadow-neon-purple/20 ring-1 ring-purple-500"
                  : "bg-zinc-900/60 border-zinc-800 hover:border-zinc-700"
              }`}
            >
              <div className="flex items-start gap-3">
                <span className="text-2xl">{item.icon}</span>
                <div>
                  <div className="text-xs font-bold text-zinc-100 group-hover:text-purple-300 transition-colors flex items-center gap-1.5">
                    <span>{item.title}</span>
                    {selectedAesthetic === item.id && (
                      <span className="w-1.5 h-1.5 rounded-full bg-purple-400 animate-ping" />
                    )}
                  </div>
                  <div className="text-[11px] text-zinc-400 mt-0.5 leading-snug">
                    {item.desc}
                  </div>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Submit Trigger */}
      <div className="pt-2 flex justify-end">
        <Button
          type="submit"
          variant="primary"
          size="lg"
          loading={loading}
          className="w-full sm:w-auto flex items-center gap-2"
        >
          <span>Synthesize IRL Loot Drop</span>
          <ArrowRight className="w-4 h-4" />
        </Button>
      </div>
    </form>
  );
};
