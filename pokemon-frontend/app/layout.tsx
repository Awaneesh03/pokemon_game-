import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Pokemon Battle Game",
  description: "Battle with Pokemon",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
