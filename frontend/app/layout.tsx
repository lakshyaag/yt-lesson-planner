// TOOD: Fix dark mode colors
import type { Metadata, Viewport } from "next";
import { Inter as FontSans } from "next/font/google";
import { ThemeProvider } from "@/components/theme-provider";
import "./globals.css";
import Header from "@/components/header";
import { cn } from "@/lib/utils";
import DotPattern from "@/components/magicui/dot-pattern";
import Footer from "@/components/footer";

const fontSans = FontSans({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "YouTube Lesson Planner",
  description: "Plan your YouTube lessons with ease.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  minimumScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={cn("font-sans antialiased", fontSans.variable)}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <DotPattern
            width={20}
            height={20}
            cx={1}
            cy={1}
            cr={1}
            className={cn(
              "[mask-image:linear-gradient(to_bottom_right,white,transparent,transparent)] "
            )}
          />

          <Header />
          <div className="flex flex-col items-center justify-center min-h-screen py-8">
            <div className="w-full max-w-4xl p-4 bg-white dark:bg-gray-800 rounded-lg">
              {children}
            </div>
          </div>
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  );
}
