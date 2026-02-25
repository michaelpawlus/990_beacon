"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";
import { ProfileHeader } from "@/components/profile/profile-header";
import { FinancialOverview } from "@/components/profile/financial-overview";
import { FinancialCharts } from "@/components/profile/financial-charts";
import { PeopleTable } from "@/components/profile/people-table";
import { GrantsTable } from "@/components/profile/grants-table";
import { MetricsCards } from "@/components/profile/metrics-cards";
import { useApi } from "@/hooks/use-api";
import type { OrganizationProfile } from "@/lib/types";

export default function OrganizationProfilePage() {
  const params = useParams<{ id: string }>();
  const api = useApi();
  const [org, setOrg] = useState<OrganizationProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!params.id) return;

    setLoading(true);
    setError(null);
    api
      .getOrganization(params.id)
      .then(setOrg)
      .catch((err) => {
        if (err.status === 404) {
          setError("Organization not found.");
        } else {
          setError("Failed to load organization data.");
        }
      })
      .finally(() => setLoading(false));
  }, [params.id, api]);

  if (loading) {
    return (
      <div className="space-y-6" data-testid="profile-loading">
        <Skeleton className="h-8 w-1/2" />
        <Skeleton className="h-4 w-1/3" />
        <div className="grid gap-4 sm:grid-cols-3">
          <Skeleton className="h-24" />
          <Skeleton className="h-24" />
          <Skeleton className="h-24" />
        </div>
      </div>
    );
  }

  if (error || !org) {
    return (
      <div className="py-16 text-center" data-testid="profile-error">
        <h2 className="text-xl font-semibold">
          {error || "Organization not found"}
        </h2>
        <p className="mt-2 text-sm text-muted-foreground">
          The organization you are looking for may not exist or may not have any
          990 filings.
        </p>
      </div>
    );
  }

  const latestFiling = org.filings[0];
  const allPeople = org.filings.flatMap((f) => f.people);
  const allGrants = org.filings.flatMap((f) => f.grants);

  return (
    <div className="space-y-8">
      <ProfileHeader org={org} />

      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="people">People</TabsTrigger>
          {allGrants.length > 0 && (
            <TabsTrigger value="grants">Grants</TabsTrigger>
          )}
        </TabsList>

        <TabsContent value="overview" className="space-y-8 pt-4">
          {latestFiling && <FinancialOverview filing={latestFiling} />}
          <FinancialCharts filings={org.filings} />
          <MetricsCards metrics={org.metrics} />
        </TabsContent>

        <TabsContent value="people" className="pt-4">
          {allPeople.length > 0 ? (
            <PeopleTable people={allPeople} />
          ) : (
            <p className="py-8 text-center text-muted-foreground">
              No personnel data available.
            </p>
          )}
        </TabsContent>

        {allGrants.length > 0 && (
          <TabsContent value="grants" className="pt-4">
            <GrantsTable grants={allGrants} />
          </TabsContent>
        )}
      </Tabs>
    </div>
  );
}
