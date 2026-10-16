import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Merge conditional class names and resolve Tailwind utility conflicts. */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/** Format an affinity score as a rounded percentage. */
export function formatAffinityScore(score: number | null | undefined): string {
  if (score == null || !Number.isFinite(score)) return "—";
  return `${Math.round(score)}%`;
}

export const formatAffinity = formatAffinityScore;

/** Turn tag IDs and underscored values into readable labels. */
export function formatTag(tag: string): string {
  return tag
    .trim()
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

/** Return badge colors for a 0–100 affinity score. */
export function getScoreColorClass(score: number): string {
  if (score >= 80) {
    return "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
  }
  if (score >= 60) {
    return "bg-cyan-500/10 text-cyan-400 border-cyan-500/30";
  }
  if (score >= 40) {
    return "bg-amber-500/10 text-amber-400 border-amber-500/30";
  }
  return "bg-zinc-500/10 text-zinc-400 border-zinc-500/30";
}
