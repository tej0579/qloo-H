import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "#08090d",
        foreground: "#f3f4f6",
        cyber: {
          dark: "#0b0d14",
          card: "#111420",
          border: "#1d2235",
          cyan: "#00f0ff",
          purple: "#9d4edd",
          pink: "#ff007f",
          emerald: "#10b981",
          amber: "#f59e0b",
          red: "#ef4444",
        },
      },
      boxShadow: {
        "neon-cyan": "0 0 20px -3px rgba(0, 240, 255, 0.4)",
        "neon-purple": "0 0 20px -3px rgba(157, 78, 221, 0.4)",
        "neon-emerald": "0 0 20px -3px rgba(16, 185, 129, 0.4)",
        "neon-pink": "0 0 20px -3px rgba(255, 0, 127, 0.4)",
        "inner-glow": "inset 0 0 15px 0 rgba(0, 240, 255, 0.15)",
      },
      backgroundImage: {
        "cyber-grid": "linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px)",
        "radial-glow": "radial-gradient(circle at 50% 0%, rgba(0, 240, 255, 0.15) 0%, transparent 60%)",
      },
    },
  },
  plugins: [],
};
export default config;
