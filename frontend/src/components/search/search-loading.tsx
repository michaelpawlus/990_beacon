import { Skeleton } from "@/components/ui/skeleton";

export function SearchLoading() {
  return (
    <div className="space-y-3" data-testid="search-loading">
      {Array.from({ length: 5 }).map((_, i) => (
        <div key={i} className="rounded-md border p-4">
          <Skeleton className="mb-2 h-5 w-3/4" />
          <Skeleton className="mb-2 h-4 w-1/2" />
          <Skeleton className="h-4 w-1/4" />
        </div>
      ))}
    </div>
  );
}
