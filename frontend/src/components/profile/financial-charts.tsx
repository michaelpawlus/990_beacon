"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { formatCompactNumber } from "@/lib/format";
import type { Filing } from "@/lib/types";

interface FinancialChartsProps {
  filings: Filing[];
}

export function FinancialCharts({ filings }: FinancialChartsProps) {
  const chartData = [...filings]
    .sort((a, b) => a.tax_year - b.tax_year)
    .map((f) => ({
      year: f.tax_year,
      revenue: f.total_revenue,
      expenses: f.total_expenses,
      netAssets: f.net_assets,
    }));

  if (chartData.length < 2) {
    return null;
  }

  return (
    <div data-testid="financial-charts">
      <h2 className="mb-4 text-lg font-semibold">Financial Trends</h2>
      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis
              tickFormatter={(value: number) => formatCompactNumber(value)}
            />
            <Tooltip
              formatter={(value: number) => formatCompactNumber(value)}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="revenue"
              stroke="#2563eb"
              name="Revenue"
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="expenses"
              stroke="#dc2626"
              name="Expenses"
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="netAssets"
              stroke="#16a34a"
              name="Net Assets"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
