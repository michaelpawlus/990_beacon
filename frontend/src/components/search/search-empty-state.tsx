import { Search } from "lucide-react";

interface SearchEmptyStateProps {
  hasQuery: boolean;
}

export function SearchEmptyState({ hasQuery }: SearchEmptyStateProps) {
  return (
    <div
      className="flex flex-col items-center justify-center py-16 text-center"
      data-testid="search-empty-state"
    >
      <Search className="mb-4 h-12 w-12 text-muted-foreground/50" />
      {hasQuery ? (
        <>
          <h3 className="text-lg font-medium">No results found</h3>
          <p className="mt-1 text-sm text-muted-foreground">
            Try adjusting your search terms or filters.
          </p>
        </>
      ) : (
        <>
          <h3 className="text-lg font-medium">Search nonprofits</h3>
          <p className="mt-1 text-sm text-muted-foreground">
            Enter a name or EIN to search IRS 990 filing data.
          </p>
        </>
      )}
    </div>
  );
}
