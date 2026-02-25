"use client";

import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { formatCurrency } from "@/lib/format";
import type { FilingPerson } from "@/lib/types";

interface PeopleTableProps {
  people: FilingPerson[];
}

export function PeopleTable({ people }: PeopleTableProps) {
  const [sortAsc, setSortAsc] = useState(false);

  if (people.length === 0) {
    return null;
  }

  const sorted = [...people].sort((a, b) => {
    const aComp = a.compensation ?? 0;
    const bComp = b.compensation ?? 0;
    return sortAsc ? aComp - bComp : bComp - aComp;
  });

  function getRoles(person: FilingPerson): string {
    const roles: string[] = [];
    if (person.is_officer) roles.push("Officer");
    if (person.is_director) roles.push("Director");
    if (person.is_key_employee) roles.push("Key Employee");
    if (person.is_highest_compensated) roles.push("Highest Compensated");
    return roles.join(", ") || "N/A";
  }

  return (
    <div data-testid="people-table">
      <h2 className="mb-4 text-lg font-semibold">
        Officers, Directors & Key Employees
      </h2>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Title</TableHead>
              <TableHead>Role</TableHead>
              <TableHead
                className="cursor-pointer text-right"
                onClick={() => setSortAsc(!sortAsc)}
              >
                Compensation {sortAsc ? "\u2191" : "\u2193"}
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sorted.map((person) => (
              <TableRow key={person.id}>
                <TableCell className="font-medium">{person.name}</TableCell>
                <TableCell>{person.title || "N/A"}</TableCell>
                <TableCell className="text-sm">{getRoles(person)}</TableCell>
                <TableCell className="text-right">
                  {formatCurrency(person.compensation)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
