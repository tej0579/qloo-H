/**
 * API bridge between the Next.js frontend and FastAPI backend.
 */

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface SendChatActionPayload {
  action: string;
  session_id?: string;
  games?: (string | any)[];
  answers?: Record<string, string>;
  message?: string;
  clarification?: any;
  query?: string;
  [key: string]: any;
}

export interface SystemHealthResponse {
  status: string;
  qloo_connected: boolean;
  qloo_latency_ms?: number;
  environment?: string;
  timestamp?: string;
  error?: string;
}

/**
 * Searches for video games to use as seed entities.
 * Calls GET `${API_BASE_URL}/api/search?query=${query}&type=urn:entity:videogame`.
 * Also falls back gracefully to `/api/qloo/search` if `/api/search` returns 404.
 */
export async function searchVideogames(query: string): Promise<any[]> {
  const trimmed = query.trim();
  if (!trimmed) return [];

  const params = new URLSearchParams({
    query: trimmed,
    type: "urn:entity:videogame",
  });

  try {
    let res = await fetch(`${API_BASE_URL}/api/search?${params.toString()}`);

    // Fallback if backend mounts qloo search at /api/qloo/search
    if (res.status === 404) {
      const fallbackParams = new URLSearchParams({
        query: trimmed,
        entity_type: "urn:entity:videogame",
      });
      res = await fetch(`${API_BASE_URL}/api/qloo/search?${fallbackParams.toString()}`);
    }

    if (!res.ok) {
      throw new Error(`Search request failed with status ${res.status}`);
    }

    const data = await res.json();
    return Array.isArray(data) ? data : data.results || [];
  } catch (error) {
    console.error("Failed to search videogames:", error);
    return [];
  }
}

/**
 * Sends a multi-turn chat action to the agent orchestrator.
 * Sends a POST request to `${API_BASE_URL}/api/chat`.
 */
export async function sendChatAction(payload: SendChatActionPayload): Promise<any> {
  const normalizedGames = payload.games
    ? payload.games.map((game) => {
        if (typeof game === "string") {
          return {
            id: "",
            name: game,
            types: ["urn:entity:videogame"],
          };
        }
        return game;
      })
    : undefined;

  const clarification =
    payload.clarification ||
    (payload.answers
      ? {
          location: payload.answers.location || "Tokyo, Japan",
          aesthetic_focus:
            payload.answers.aesthetic_focus ||
            payload.answers.aesthetic ||
            "streetwear_audio",
        }
      : undefined);

  const body: Record<string, any> = {
    action: payload.action,
    session_id: payload.session_id,
    games: normalizedGames,
    clarification,
    query: payload.query || payload.message,
  };

  const res = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errorText = await res.text().catch(() => "");
    throw new Error(
      `Chat action failed with status ${res.status}: ${errorText || res.statusText}`
    );
  }

  return res.json();
}

/**
 * Retrieves cached loot drop or conversation state for an active session.
 * Calls GET `${API_BASE_URL}/api/session/${sessionId}`.
 */
export async function fetchSessionLoot(sessionId: string): Promise<any> {
  const res = await fetch(
    `${API_BASE_URL}/api/session/${encodeURIComponent(sessionId)}`
  );

  if (!res.ok) {
    throw new Error(
      `Failed to fetch session loot with status ${res.status}: ${res.statusText}`
    );
  }

  return res.json();
}

/**
 * Checks system health and Qloo API connectivity.
 * Calls GET `${API_BASE_URL}/api/health` and catches connection errors safely.
 */
export async function checkSystemHealth(): Promise<SystemHealthResponse> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/health`);
    if (!res.ok) {
      return {
        status: "unhealthy",
        qloo_connected: false,
        error: `Health check returned status ${res.status}`,
      };
    }
    return await res.json();
  } catch (error) {
    return {
      status: "disconnected",
      qloo_connected: false,
      error: error instanceof Error ? error.message : "Connection failed",
    };
  }
}

/**
 * Alias for checkSystemHealth for backward compatibility.
 */
export const fetchHealth = checkSystemHealth;
