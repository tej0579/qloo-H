import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "cyan" | "purple" | "emerald" | "pink" | "amber" | "muted" | "outline";
}

export const Badge: React.FC<BadgeProps> = ({
  className,
  variant = "cyan",
  children,
  ...props
}) => {
  const variantClasses = {
    cyan: "bg-cyber-cyan/10 text-cyber-cyan border-cyber-cyan/30 shadow-[0_0_10px_rgba(0,240,255,0.2)]",
    purple: "bg-purple-500/10 text-purple-400 border-purple-500/30 shadow-[0_0_10px_rgba(157,78,221,0.2)]",
    emerald: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30 shadow-[0_0_10px_rgba(16,185,129,0.2)]",
    pink: "bg-pink-500/10 text-pink-400 border-pink-500/30 shadow-[0_0_10px_rgba(255,0,127,0.2)]",
    amber: "bg-amber-500/10 text-amber-400 border-amber-500/30",
    muted: "bg-zinc-800/80 text-zinc-400 border-zinc-700/60",
    outline: "bg-transparent text-zinc-300 border-zinc-700",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border tracking-wide uppercase",
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};
