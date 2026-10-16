import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Tailwind CSS class merger utility using clsx and tailwind-merge.
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/**
 * Normalizes an affinity decimal or percentage number into a display percentage string.
 * E.g., 0.94 -> "94%", 94 -> "94%". Defaults to "92%" if undefined or null.
 */
export function formatAffinityScore(score?: number): string {
  if (score === undefined || score === null || Number.isNaN(score)) {
    return "92%";
  }
  const normalized = score <= 1 && score >= 0 ? score * 100 : score;
  return `${Math.round(normalized)}%`;
}

/**
 * Alias for formatAffinityScore for backwards compatibility.
 */
export const formatAffinity = formatAffinityScore;

/**
 * Cleans Qloo URN tags:
 * - Strips "urn:tag:" prefix
 * - Converts underscores and hyphens to spaces
 * - Capitalizes each word
 *
 * E.g., "urn:tag:cyberpunk_streetwear" -> "Cyberpunk Streetwear"
 *       "urn:tag:neo-tokyo" -> "Neo Tokyo"
 */
export function formatTag(tag: string): string {
  if (!tag) return "";
  return tag
    .replace(/^urn:tag:/i, "")
    .replace(/[_-]+/g, " ")
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
}

/**
 * Returns Tailwind CSS styling classes based on affinity score threshold.
 */
export function getScoreColorClass(score?: number): string {
  const normalized =
    score === undefined || score === null || Number.isNaN(score)
      ? 92
      : score <= 1 && score >= 0
      ? score * 100
      : score;

  if (normalized >= 90) {
    return "bg-cyber-cyan/10 text-cyber-cyan border-cyber-cyan/40 shadow-[0_0_10px_rgba(0,240,255,0.2)]";
  }
  if (normalized >= 80) {
    return "bg-purple-500/10 text-purple-400 border-purple-500/40 shadow-[0_0_10px_rgba(157,78,221,0.2)]";
  }
  if (normalized >= 70) {
    return "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
  }
  if (normalized >= 60) {
    return "bg-amber-500/10 text-amber-400 border-amber-500/30";
  }
  return "bg-zinc-800 text-zinc-400 border-zinc-700";
}
