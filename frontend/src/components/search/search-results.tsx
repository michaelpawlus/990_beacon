"use client";

import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { formatCompactNumber } from "@/lib/format";
import type { OrganizationSearchResult } from "@/lib/types";

interface SearchResultsProps {
  results: OrganizationSearchResult[];
}

export function SearchResults({ results }: SearchResultsProps) {
  return (
    <div className="space-y-2" data-testid="search-results">
      {results.map((org) => (
        <Link
          key={org.id}
          href={`/dashboard/organizations/${org.id}`}
          className="block rounded-md border p-4 transition-colors hover:bg-accent/50"
        >
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0 flex-1">
              <h3 className="font-semibold">{org.name}</h3>
              <p className="text-sm text-muted-foreground">
                EIN: {org.ein}
                {org.city && org.state ? ` | ${org.city}, ${org.state}` : ""}
              </p>
            </div>
            <div className="flex flex-shrink-0 items-center gap-2">
              {org.ntee_code && (
                <Badge variant="secondary">{org.ntee_code}</Badge>
              )}
              {org.latest_tax_year && (
                <Badge variant="outline">{org.latest_tax_year}</Badge>
              )}
            </div>
          </div>
          {org.latest_revenue != null && (
            <p className="mt-1 text-sm text-muted-foreground">
              Revenue: {formatCompactNumber(org.latest_revenue)}
            </p>
          )}
        </Link>
      ))}
    </div>
  );
}
