"use client";

import { useState, useCallback } from "react";
import { UserGameSelection, ClarificationAnswer } from "@/types/agent";
import { LootDropPayload } from "@/types/loot";
import { sendChatAction } from "@/lib/api";

export function useAgentChat() {
  const [sessionId, setSessionId] = useState<string>("");
  const [selectedGames, setSelectedGames] = useState<UserGameSelection[]>([]);
  const [lootDrop, setLootDrop] = useState<LootDropPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const reset = useCallback(() => {
    setSelectedGames([]);
    setLootDrop(null);
    setError(null);
    if (sessionId) {
      sendChatAction({ session_id: sessionId, action: "RESET" }).catch(console.error);
    }
  }, [sessionId]);

  return {
    sessionId,
    setSessionId,
    selectedGames,
    setSelectedGames,
    lootDrop,
    setLootDrop,
    loading,
    setLoading,
    error,
    setError,
    reset,
  };
}
