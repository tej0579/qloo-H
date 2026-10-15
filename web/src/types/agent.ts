import { LootDropPayload } from "./loot";

export interface UserGameSelection {
  id: string;
  name: string;
  types?: string[];
  entity_id?: string;
}

export interface ClarificationOption {
  id: string;
  label: string;
  description?: string;
}

export interface ClarificationQuestion {
  id: string;
  step: number;
  title: string;
  prompt: string;
  options: ClarificationOption[];
  default_value?: string;
}

export interface ClarificationAnswer {
  location: string;
  aesthetic_focus: string;
}

export interface ChatRequest {
  session_id?: string;
  action?: "SEED_GAMES" | "CLARIFY" | "EXECUTE" | "RESET";
  games?: UserGameSelection[];
  query?: string;
  clarification?: ClarificationAnswer;
}

export interface ChatResponse {
  session_id: string;
  status: "AWAITING_INPUT" | "AWAITING_CLARIFICATION" | "COMPLETED" | "RESET" | "ERROR";
  action: string;
  message: string;
  verified_games?: UserGameSelection[];
  clarification_questions?: ClarificationQuestion[];
  lootdrop?: LootDropPayload;
}
