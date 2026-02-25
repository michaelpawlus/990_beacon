"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { SearchFilters } from "@/lib/types";

const US_STATES = [
  "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL",
  "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
  "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
  "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR",
  "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
  "WI", "WY",
];

interface FilterPanelProps {
  filters: SearchFilters;
  onApply: (filters: SearchFilters) => void;
}

export function FilterPanel({ filters, onApply }: FilterPanelProps) {
  const [expanded, setExpanded] = useState(false);
  const [localFilters, setLocalFilters] = useState<SearchFilters>(filters);

  function handleApply() {
    onApply(localFilters);
  }

  function handleClear() {
    const cleared: SearchFilters = { q: filters.q };
    setLocalFilters(cleared);
    onApply(cleared);
  }

  const hasActiveFilters =
    localFilters.state ||
    localFilters.ntee_code ||
    localFilters.min_revenue ||
    localFilters.max_revenue ||
    localFilters.min_assets ||
    localFilters.max_assets ||
    localFilters.filing_year;

  return (
    <div className="rounded-md border p-4" data-testid="filter-panel">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between text-sm font-medium"
        data-testid="filter-toggle"
      >
        <span>
          Filters{" "}
          {hasActiveFilters && (
            <span className="ml-1 text-xs text-muted-foreground">(active)</span>
          )}
        </span>
        {expanded ? (
          <ChevronUp className="h-4 w-4" />
        ) : (
          <ChevronDown className="h-4 w-4" />
        )}
      </button>

      {expanded && (
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <div>
            <Label htmlFor="state-filter">State</Label>
            <select
              id="state-filter"
              value={localFilters.state || ""}
              onChange={(e) =>
                setLocalFilters({ ...localFilters, state: e.target.value || undefined })
              }
              className="mt-1 w-full rounded-md border bg-background px-3 py-2 text-sm"
            >
              <option value="">All States</option>
              {US_STATES.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>

          <div>
            <Label htmlFor="ntee-filter">NTEE Code</Label>
            <Input
              id="ntee-filter"
              placeholder="e.g. P20"
              value={localFilters.ntee_code || ""}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  ntee_code: e.target.value || undefined,
                })
              }
              className="mt-1"
            />
          </div>

          <div>
            <Label htmlFor="filing-year-filter">Filing Year</Label>
            <Input
              id="filing-year-filter"
              type="number"
              placeholder="e.g. 2023"
              value={localFilters.filing_year ?? ""}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  filing_year: e.target.value
                    ? Number(e.target.value)
                    : undefined,
                })
              }
              className="mt-1"
            />
          </div>

          <div>
            <Label htmlFor="min-revenue-filter">Min Revenue</Label>
            <Input
              id="min-revenue-filter"
              type="number"
              placeholder="0"
              value={localFilters.min_revenue ?? ""}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  min_revenue: e.target.value
                    ? Number(e.target.value)
                    : undefined,
                })
              }
              className="mt-1"
            />
          </div>

          <div>
            <Label htmlFor="max-revenue-filter">Max Revenue</Label>
            <Input
              id="max-revenue-filter"
              type="number"
              placeholder="No limit"
              value={localFilters.max_revenue ?? ""}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  max_revenue: e.target.value
                    ? Number(e.target.value)
                    : undefined,
                })
              }
              className="mt-1"
            />
          </div>

          <div>
            <Label htmlFor="min-assets-filter">Min Assets</Label>
            <Input
              id="min-assets-filter"
              type="number"
              placeholder="0"
              value={localFilters.min_assets ?? ""}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  min_assets: e.target.value
                    ? Number(e.target.value)
                    : undefined,
                })
              }
              className="mt-1"
            />
          </div>

          <div>
            <Label htmlFor="max-assets-filter">Max Assets</Label>
            <Input
              id="max-assets-filter"
              type="number"
              placeholder="No limit"
              value={localFilters.max_assets ?? ""}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  max_assets: e.target.value
                    ? Number(e.target.value)
                    : undefined,
                })
              }
              className="mt-1"
            />
          </div>

          <div className="flex items-end gap-2 sm:col-span-2 lg:col-span-3">
            <Button onClick={handleApply} size="sm">
              Apply Filters
            </Button>
            {hasActiveFilters && (
              <button
                onClick={handleClear}
                className="flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
              >
                <X className="h-3 w-3" />
                Clear
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
