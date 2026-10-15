import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "IRL LootDrop | Qloo Cultural Intelligence for Gamers",
  description:
    "Translating video game obsessions into real-world lifestyle profiles, fashion, audio, and physical sanctuaries using Qloo Taste Intelligence.",
  icons: {
    icon: "/lootdrop-symbol.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-cyber-dark text-zinc-100 flex flex-col antialiased selection:bg-cyber-cyan selection:text-black">
        <div className="fixed inset-0 bg-cyber-grid bg-[size:40px_40px] pointer-events-none opacity-40 z-0" />
        <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[300px] bg-cyber-cyan/5 blur-[120px] pointer-events-none z-0" />
        <div className="relative z-10 flex-1 flex flex-col">{children}</div>
      </body>
    </html>
  );
}
