"use client";

import { useAuth } from "@clerk/nextjs";
import { useMemo } from "react";
import { createApiClient } from "@/lib/api-client";
import type { SearchFilters } from "@/lib/types";

export function useApi() {
  const { getToken } = useAuth();

  const api = useMemo(() => {
    return {
      async getMe() {
        const token = (await getToken()) ?? undefined;
        return createApiClient(token).getMe();
      },
      async getHealth() {
        return createApiClient().getHealth();
      },
      async searchOrganizations(filters: SearchFilters) {
        const token = (await getToken()) ?? undefined;
        return createApiClient(token).searchOrganizations(filters);
      },
      async typeahead(q: string) {
        const token = (await getToken()) ?? undefined;
        return createApiClient(token).typeahead(q);
      },
      async getOrganization(id: string) {
        const token = (await getToken()) ?? undefined;
        return createApiClient(token).getOrganization(id);
      },
      async getUsageSummary() {
        const token = (await getToken()) ?? undefined;
        return createApiClient(token).getUsageSummary();
      },
    };
  }, [getToken]);

  return api;
}
