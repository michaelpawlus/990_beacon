import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
          <h1 className="text-xl font-bold">990 Beacon</h1>
          <div className="flex gap-2">
            <Button variant="ghost" asChild>
              <Link href="/sign-in">Sign In</Link>
            </Button>
            <Button asChild>
              <Link href="/sign-up">Get Started</Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex flex-1 flex-col items-center justify-center px-4">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-4xl font-bold tracking-tight sm:text-5xl">
            Nonprofit Intelligence, Simplified
          </h2>
          <p className="mt-6 text-lg text-muted-foreground">
            Transform IRS 990 filing data into actionable insights. Search
            millions of nonprofits, track financial health, and discover
            grant-making patterns — all in one platform.
          </p>

          <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <Button size="lg" asChild>
              <Link href="/sign-up">Start Free Trial</Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="/sign-in">Sign In</Link>
            </Button>
          </div>

          <div className="mt-16 grid gap-8 sm:grid-cols-3">
            <div className="rounded-lg border p-6 text-left">
              <h3 className="font-semibold">Search &amp; Explore</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                Full-text search across all e-filed 990s with powerful filters.
              </p>
            </div>
            <div className="rounded-lg border p-6 text-left">
              <h3 className="font-semibold">Financial Health Scores</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                Algorithmic scoring based on revenue diversity, reserves, and
                efficiency.
              </p>
            </div>
            <div className="rounded-lg border p-6 text-left">
              <h3 className="font-semibold">AI Summaries</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                LLM-generated narrative analysis for every organization.
              </p>
            </div>
          </div>
        </div>
      </main>

      <footer className="border-t py-6 text-center text-sm text-muted-foreground">
        &copy; 2026 990 Beacon. All rights reserved.
      </footer>
    </div>
  );
}
