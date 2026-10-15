import React from "react";
import { LootDropItem } from "@/types/loot";
import { formatAffinity, getScoreColorClass } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Sparkles, MapPin, DollarSign, Tag } from "lucide-react";

interface VibeCardProps {
  item: LootDropItem;
}

export const VibeCard: React.FC<VibeCardProps> = ({ item }) => {
  return (
    <div className="group relative rounded-xl bg-cyber-card/80 backdrop-blur-md border border-zinc-800 p-4 hover:border-cyber-cyan/50 hover:shadow-neon-cyan/15 transition-all duration-300 flex flex-col justify-between">
      {/* Top Meta: Category & Affinity Score */}
      <div>
        <div className="flex items-center justify-between gap-2 pb-2">
          <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 flex items-center gap-1">
            <Tag className="w-3 h-3 text-purple-400" />
            {item.category}
          </span>
          <span
            className={`px-2 py-0.5 rounded-full text-[11px] font-bold font-mono border ${getScoreColorClass(
              item.affinity_score
            )}`}
          >
            {formatAffinity(item.affinity_score)} Affinity
          </span>
        </div>

        {/* Entity Title */}
        <h4 className="text-base font-bold text-zinc-100 group-hover:text-cyber-cyan transition-colors">
          {item.name}
        </h4>

        {/* Description */}
        {item.description && (
          <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
            {item.description}
          </p>
        )}
      </div>

      {/* Middle: Location & Price if applicable */}
      <div className="pt-3 space-y-2">
        {(item.location || item.price_level) && (
          <div className="flex items-center gap-3 text-[11px] text-zinc-400 pt-1 border-t border-zinc-800/80">
            {item.location && (
              <span className="flex items-center gap-1 truncate text-zinc-300">
                <MapPin className="w-3 h-3 text-cyber-cyan shrink-0" />
                <span className="truncate">{item.location}</span>
              </span>
            )}
            {item.price_level && (
              <span className="flex items-center gap-0.5 font-mono text-emerald-400">
                <DollarSign className="w-3 h-3 shrink-0" />
                <span>{item.price_level}</span>
              </span>
            )}
          </div>
        )}

        {/* Cultural Tags Badges */}
        {item.tags && item.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 pt-1">
            {item.tags.slice(0, 3).map((tag, idx) => (
              <Badge key={idx} variant="cyan" className="text-[10px] py-0">
                {tag}
              </Badge>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
