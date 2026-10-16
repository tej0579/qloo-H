import type { ChatRequest, ChatResponse } from "@/types/agent";
import type { LootDropPayload } from "@/types/loot";
import type { QlooEntity, QlooSearchResult } from "@/types/qloo";

const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
).replace(/\/+$/, "");

export interface SystemHealth {
  status: string;
  qloo_connected: boolean;
  qloo_latency_ms?: number | null;
  environment?: string;
  timestamp?: string;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      ...(init?.body ? { "Content-Type": "application/json" } : {}),
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`API request failed (${response.status}): ${detail}`);
  }

  return response.json() as Promise<T>;
}

export async function searchVideogames(query: string): Promise<QlooEntity[]> {
  const params = new URLSearchParams({
    query,
    limit: "10",
    entity_type: "urn:entity:videogame",
  });
  const result = await request<QlooSearchResult>(`/api/qloo/search?${params}`);
  return result.results;
}

export function sendChatAction(payload: ChatRequest): Promise<ChatResponse> {
  return request<ChatResponse>("/api/chat", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function fetchSessionLoot(sessionId: string): Promise<LootDropPayload> {
  const session = await request<{
    lootdrop_payload?: LootDropPayload | null;
    lootdrop?: LootDropPayload | null;
  }>(`/api/session/${encodeURIComponent(sessionId)}`);
  const payload = session.lootdrop_payload ?? session.lootdrop;
  if (!payload) throw new Error(`No LootDrop payload found for session ${sessionId}`);
  return payload;
}

export function checkSystemHealth(): Promise<SystemHealth> {
  return request<SystemHealth>("/api/health");
}

export const fetchHealth = checkSystemHealth;
