"use client";

import { UserButton } from "@clerk/nextjs";

export function UserMenu() {
  return (
    <div data-testid="user-menu">
      <UserButton afterSignOutUrl="/" />
    </div>
  );
}
