"use client";

import { useAuth } from "@clerk/nextjs";
import { useMemo } from "react";
import { createApiClient } from "@/lib/api-client";

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
    };
  }, [getToken]);

  return api;
}
