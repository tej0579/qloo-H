"use client";

import { useState } from "react";
import { LootDropPayload } from "@/types/loot";

export function useLootDrop() {
  const [currentDrop, setCurrentDrop] = useState<LootDropPayload | null>(null);

  const saveDrop = (drop: LootDropPayload) => {
    setCurrentDrop(drop);
    try {
      localStorage.setItem("irl_last_lootdrop", JSON.stringify(drop));
    } catch (e) {
      // LocalStorage fallback
    }
  };

  const loadSavedDrop = (): LootDropPayload | null => {
    try {
      const saved = localStorage.getItem("irl_last_lootdrop");
      if (saved) return JSON.parse(saved);
    } catch (e) {
      // ignore
    }
    return null;
  };

  return {
    currentDrop,
    setCurrentDrop: saveDrop,
    loadSavedDrop,
  };
}
