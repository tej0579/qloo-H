export interface LootDropItem {
  id: string;
  name: string;
  category: string;
  affinity_score: number | null;
  tags: string[];
  description?: string;
  location?: string;
  price_level?: string;
  properties?: Record<string, any>;
}

export interface LootDropCategory {
  id: string;
  display_title: string;
  icon: string;
  description: string;
  items: LootDropItem[];
}

export interface QuestLogStep {
  time: string;
  title: string;
  recommendation: string;
  description: string;
}

export interface ComparatorItem {
  category: string;
  item_name: string;
  detail: string;
  vibe_or_tag: string;
  score?: number;
}

export interface ComparatorComparison {
  dimension: string;
  unassisted_llm_cliche: string;
  qloo_grounded_reality: string;
  why_it_matters: string;
  cultural_tag_contrast?: Record<string, string>;
}

export interface ComparatorPayload {
  unassisted_llm_response: ComparatorItem[];
  qloo_grounded_response: ComparatorItem[];
  comparisons: ComparatorComparison[];
  summary_verdict: string;
}

export interface RadarMetric {
  subject: string;
  qloo_affinity: number | null;
  llm_relevance: number | null;
}

export interface LootDropPayload {
  session_id: string;
  seed_games: { id: string; name: string; types: string[] }[];
  persona_title: string;
  persona_description: string;
  archetype_title?: string;
  quest_log?: QuestLogStep[];
  location?: string;
  aesthetic_focus?: string;
  categories: LootDropCategory[];
  comparator: ComparatorPayload;
  radar_metrics: RadarMetric[];
  data_source: "qloo_live" | "demo_fallback";
  overall_match_score: number | null;
  created_at: string;
}
