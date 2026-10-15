import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger" | "neon";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", loading, children, disabled, ...props }, ref) => {
    const baseClasses =
      "inline-flex items-center justify-center font-medium transition-all duration-200 rounded-lg select-none disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-cyber-cyan/50";

    const sizeClasses = {
      sm: "px-3 py-1.5 text-xs font-semibold tracking-wider",
      md: "px-4 py-2 text-sm font-semibold tracking-wide",
      lg: "px-6 py-3 text-base font-bold tracking-wider",
    };

    const variantClasses = {
      primary:
        "bg-gradient-to-r from-cyber-cyan to-blue-600 text-black font-bold shadow-neon-cyan hover:brightness-110 active:scale-[0.98]",
      neon: "bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold shadow-neon-purple hover:brightness-110 active:scale-[0.98]",
      secondary:
        "bg-zinc-800 text-zinc-100 hover:bg-zinc-700 border border-zinc-700 active:scale-[0.98]",
      outline:
        "bg-transparent text-cyber-cyan border border-cyber-cyan/50 hover:bg-cyber-cyan/10 hover:border-cyber-cyan active:scale-[0.98]",
      ghost:
        "bg-transparent text-zinc-400 hover:text-white hover:bg-zinc-800/60 active:scale-[0.98]",
      danger:
        "bg-red-500/20 text-red-400 border border-red-500/40 hover:bg-red-500/30 active:scale-[0.98]",
    };

    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(baseClasses, sizeClasses[size], variantClasses[variant], className)}
        {...props}
      >
        {loading ? (
          <span className="flex items-center gap-2">
            <svg
              className="animate-spin h-4 w-4"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8H4z"
              />
            </svg>
            <span>Processing...</span>
          </span>
        ) : (
          children
        )}
      </button>
    );
  }
);
Button.displayName = "Button";
