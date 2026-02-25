"use client";

import { useState, useCallback } from "react";
import { SearchBar } from "@/components/search/search-bar";
import { FilterPanel } from "@/components/search/filter-panel";
import { SearchResults } from "@/components/search/search-results";
import { SearchPagination } from "@/components/search/search-pagination";
import { SearchEmptyState } from "@/components/search/search-empty-state";
import { SearchLoading } from "@/components/search/search-loading";
import { useApi } from "@/hooks/use-api";
import type {
  SearchFilters,
  OrganizationSearchResult,
  PaginatedResults,
} from "@/lib/types";

export default function SearchPage() {
  const api = useApi();
  const [filters, setFilters] = useState<SearchFilters>({});
  const [results, setResults] =
    useState<PaginatedResults<OrganizationSearchResult> | null>(null);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const performSearch = useCallback(
    async (searchFilters: SearchFilters) => {
      setLoading(true);
      setHasSearched(true);
      try {
        const data = await api.searchOrganizations(searchFilters);
        setResults(data);
      } catch {
        setResults(null);
      } finally {
        setLoading(false);
      }
    },
    [api]
  );

  function handleSearch(query: string) {
    const updated = { ...filters, q: query, page: 1 };
    setFilters(updated);
    performSearch(updated);
  }

  function handleFilterApply(newFilters: SearchFilters) {
    const updated = { ...newFilters, page: 1 };
    setFilters(updated);
    if (hasSearched || updated.q) {
      performSearch(updated);
    }
  }

  function handlePageChange(page: number) {
    const updated = { ...filters, page };
    setFilters(updated);
    performSearch(updated);
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Search Organizations</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Search IRS 990 filing data for nonprofit organizations.
        </p>
      </div>

      <SearchBar initialQuery={filters.q} onSearch={handleSearch} />

      <FilterPanel filters={filters} onApply={handleFilterApply} />

      {loading && <SearchLoading />}

      {!loading && results && results.items.length > 0 && (
        <>
          <div className="text-sm text-muted-foreground">
            {results.total} result{results.total !== 1 ? "s" : ""} found
          </div>
          <SearchResults results={results.items} />
          <SearchPagination
            page={results.page}
            totalPages={results.total_pages}
            onPageChange={handlePageChange}
          />
        </>
      )}

      {!loading && hasSearched && results?.items.length === 0 && (
        <SearchEmptyState hasQuery={!!filters.q} />
      )}

      {!loading && !hasSearched && <SearchEmptyState hasQuery={false} />}
    </div>
  );
}
