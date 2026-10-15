import * as React from "react";
import { cn } from "@/lib/utils";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  glow?: "cyan" | "purple" | "emerald" | "none";
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, glow = "none", children, ...props }, ref) => {
    const glowClasses = {
      cyan: "border-cyber-cyan/30 shadow-neon-cyan/20",
      purple: "border-purple-500/30 shadow-neon-purple/20",
      emerald: "border-emerald-500/30 shadow-neon-emerald/20",
      none: "border-zinc-800/80 hover:border-zinc-700",
    };

    return (
      <div
        ref={ref}
        className={cn(
          "rounded-xl bg-cyber-card/90 backdrop-blur-md border p-5 transition-all duration-300",
          glowClasses[glow],
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Card.displayName = "Card";
