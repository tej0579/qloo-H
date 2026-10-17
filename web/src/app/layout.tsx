import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Qloo Videogame Cultural Intelligence Agent",
  description: "Category 1/14: Multi-turn taste calibration and grounded synthesis using Qloo Taste Graph.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-[#090a0f] text-zinc-200">
        {children}
      </body>
    </html>
  );
}
