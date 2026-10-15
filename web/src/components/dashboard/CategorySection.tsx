"use client";

import React, { useState } from "react";
import { LootDropCategory } from "@/types/loot";
import { VibeCard } from "./VibeCard";
import { Shirt, Headphones, MapPin, Film, Layers } from "lucide-react";

interface CategorySectionProps {
  categories: LootDropCategory[];
}

export const CategorySection: React.FC<CategorySectionProps> = ({ categories }) => {
  const [selectedTab, setSelectedTab] = useState<string>("all");

  const getIcon = (iconName: string) => {
    switch (iconName.toLowerCase()) {
      case "shirt":
        return <Shirt className="w-4 h-4 text-cyber-cyan" />;
      case "headphones":
        return <Headphones className="w-4 h-4 text-purple-400" />;
      case "mappin":
        return <MapPin className="w-4 h-4 text-emerald-400" />;
      case "film":
        return <Film className="w-4 h-4 text-pink-400" />;
      default:
        return <Layers className="w-4 h-4 text-zinc-400" />;
    }
  };

  const displayedCategories =
    selectedTab === "all"
      ? categories
      : categories.filter((c) => c.id === selectedTab);

  return (
    <div className="space-y-6">
      {/* Category Tab Selector */}
      <div className="flex flex-wrap items-center gap-2 pb-2 border-b border-zinc-800">
        <button
          onClick={() => setSelectedTab("all")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
            selectedTab === "all"
              ? "bg-zinc-100 text-black shadow-md"
              : "bg-zinc-900/80 text-zinc-400 hover:text-white hover:bg-zinc-800"
          }`}
        >
          <Layers className="w-3.5 h-3.5" />
          <span>All Loot ({categories.reduce((acc, c) => acc + c.items.length, 0)})</span>
        </button>

        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setSelectedTab(cat.id)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              selectedTab === cat.id
                ? "bg-cyber-cyan text-black font-bold shadow-neon-cyan"
                : "bg-zinc-900/80 text-zinc-400 hover:text-white hover:bg-zinc-800 border border-zinc-800/80"
            }`}
          >
            {getIcon(cat.icon)}
            <span>{cat.display_title.split("&")[0].trim()}</span>
            <span className="text-[10px] px-1 py-0.2 rounded bg-black/40 text-zinc-300">
              {cat.items.length}
            </span>
          </button>
        ))}
      </div>

      {/* Rendered Categories */}
      <div className="space-y-8">
        {displayedCategories.map((cat) => (
          <div key={cat.id} className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {getIcon(cat.icon)}
                <h3 className="text-base font-bold text-zinc-100">
                  {cat.display_title}
                </h3>
              </div>
              <span className="text-xs text-zinc-400 hidden sm:block">
                {cat.description}
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {cat.items.map((item) => (
                <VibeCard key={item.id} item={item} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
