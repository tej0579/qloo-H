"use client";

import React, { useState } from "react";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { AgentChat } from "@/components/agent/AgentChat";
import { LootDashboard } from "@/components/dashboard/LootDashboard";
import { LootDropPayload } from "@/types/loot";

export default function Home() {
  const [activeView, setActiveView] = useState<"agent" | "dashboard">("agent");
  const [lootDrop, setLootDrop] = useState<LootDropPayload | null>(null);

  const handleLootDropReady = (payload: LootDropPayload) => {
    setLootDrop(payload);
    setActiveView("dashboard");
  };

  const handleReset = () => {
    setLootDrop(null);
    setActiveView("agent");
  };

  return (
    <div className="flex-1 flex flex-col justify-between">
      <Header
        activeView={activeView}
        onViewChange={setActiveView}
        hasLootDrop={Boolean(lootDrop)}
      />

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 w-full">
        {activeView === "agent" ? (
          <AgentChat onLootDropReady={handleLootDropReady} />
        ) : lootDrop ? (
          <LootDashboard payload={lootDrop} onReset={handleReset} />
        ) : (
          <AgentChat onLootDropReady={handleLootDropReady} />
        )}
      </main>

      <Footer />
    </div>
  );
}
