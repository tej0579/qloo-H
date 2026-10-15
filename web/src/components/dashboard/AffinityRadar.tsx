"use client";

import React, { useEffect, useState } from "react";
import { RadarMetric } from "@/types/loot";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";
import { Activity } from "lucide-react";

interface AffinityRadarProps {
  metrics: RadarMetric[];
}

export const AffinityRadar: React.FC<AffinityRadarProps> = ({ metrics }) => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="h-72 w-full flex items-center justify-center text-xs text-zinc-500 font-mono">
        Loading Radar Visualization...
      </div>
    );
  }

  const chartData = metrics.map((m) => ({
    subject: m.subject,
    "Qloo Affinity": m.qloo_affinity,
    "Standard LLM": m.llm_relevance,
    fullMark: 100,
  }));

  return (
    <div className="rounded-2xl bg-cyber-card/80 backdrop-blur-xl border border-zinc-800 p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-cyber-cyan" />
          <h3 className="text-sm font-bold text-zinc-100">
            Cross-Domain Affinity Footprint
          </h3>
        </div>
        <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700">
          Normalized Index
        </span>
      </div>

      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={chartData}>
            <PolarGrid stroke="#27272a" />
            <PolarAngleAxis
              dataKey="subject"
              tick={{ fill: "#a1a1aa", fontSize: 11, fontWeight: 500 }}
            />
            <PolarRadiusAxis
              angle={30}
              domain={[0, 100]}
              tick={{ fill: "#71717a", fontSize: 9 }}
              stroke="#27272a"
            />
            <Radar
              name="Qloo Taste Graph"
              dataKey="Qloo Affinity"
              stroke="#00f0ff"
              fill="#00f0ff"
              fillOpacity={0.4}
            />
            <Radar
              name="Standard LLM Cliché"
              dataKey="Standard LLM"
              stroke="#ef4444"
              fill="#ef4444"
              fillOpacity={0.2}
              strokeDasharray="4 4"
            />
            <Legend
              wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }}
              formatter={(value) => (
                <span className="text-zinc-300 font-medium">{value}</span>
              )}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0b0d14",
                borderColor: "#27272a",
                borderRadius: "8px",
                fontSize: "12px",
                color: "#f3f4f6",
              }}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      <p className="text-[11px] text-zinc-500 text-center font-mono">
        Higher polygon area represents authentic subcultural engagement outside the game.
      </p>
    </div>
  );
};
