"use client";

import { useEffect, useState } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import { useApi } from "@/hooks/use-api";
import type { UsageSummary } from "@/lib/types";

export default function SettingsPage() {
  const api = useApi();
  const [usage, setUsage] = useState<UsageSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getUsageSummary()
      .then(setUsage)
      .catch(() => setUsage(null))
      .finally(() => setLoading(false));
  }, [api]);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Account settings and usage overview.
        </p>
      </div>

      <section data-testid="usage-section">
        <h2 className="text-lg font-semibold">Usage</h2>
        <p className="mb-4 text-sm text-muted-foreground">
          Your activity for the current period.
        </p>

        {loading ? (
          <div className="grid gap-4 sm:grid-cols-2" data-testid="usage-loading">
            <Skeleton className="h-24" />
            <Skeleton className="h-24" />
            <Skeleton className="h-24" />
            <Skeleton className="h-24" />
          </div>
        ) : usage ? (
          <div className="grid gap-4 sm:grid-cols-2" data-testid="usage-cards">
            <UsageCard
              label="Searches today"
              value={usage.searches_today}
              testId="searches-today"
            />
            <UsageCard
              label="Searches this month"
              value={usage.searches_this_month}
              testId="searches-month"
            />
            <UsageCard
              label="Profile views today"
              value={usage.profile_views_today}
              testId="views-today"
            />
            <UsageCard
              label="Profile views this month"
              value={usage.profile_views_this_month}
              testId="views-month"
            />
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">
            Unable to load usage data.
          </p>
        )}
      </section>

      <section>
        <h2 className="text-lg font-semibold">Account</h2>
        <p className="text-sm text-muted-foreground">
          Account management coming in Phase 4.
        </p>
      </section>
    </div>
  );
}

function UsageCard({
  label,
  value,
  testId,
}: {
  label: string;
  value: number;
  testId: string;
}) {
  return (
    <div
      className="rounded-lg border p-4"
      data-testid={testId}
    >
      <p className="text-sm text-muted-foreground">{label}</p>
      <p className="mt-1 text-2xl font-bold">{value.toLocaleString()}</p>
    </div>
  );
}
