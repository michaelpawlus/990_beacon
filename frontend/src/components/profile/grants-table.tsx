"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { formatCurrency } from "@/lib/format";
import type { FilingGrant } from "@/lib/types";

interface GrantsTableProps {
  grants: FilingGrant[];
}

export function GrantsTable({ grants }: GrantsTableProps) {
  if (grants.length === 0) {
    return null;
  }

  return (
    <div data-testid="grants-table">
      <h2 className="mb-4 text-lg font-semibold">Grants Awarded</h2>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Recipient</TableHead>
              <TableHead>Location</TableHead>
              <TableHead>Purpose</TableHead>
              <TableHead className="text-right">Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {grants.map((grant) => (
              <TableRow key={grant.id}>
                <TableCell>
                  <div className="font-medium">{grant.recipient_name}</div>
                  {grant.recipient_ein && (
                    <div className="text-xs text-muted-foreground">
                      EIN: {grant.recipient_ein}
                    </div>
                  )}
                </TableCell>
                <TableCell>
                  {grant.recipient_city && grant.recipient_state
                    ? `${grant.recipient_city}, ${grant.recipient_state}`
                    : "N/A"}
                </TableCell>
                <TableCell className="max-w-xs truncate text-sm">
                  {grant.purpose || "N/A"}
                </TableCell>
                <TableCell className="text-right">
                  {formatCurrency(grant.amount)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
