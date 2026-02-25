import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatPercent } from "@/lib/format";
import type { ComputedMetrics } from "@/lib/types";

interface MetricsCardsProps {
  metrics: ComputedMetrics;
}

export function MetricsCards({ metrics }: MetricsCardsProps) {
  const items = [
    {
      label: "Program Expense Ratio",
      value: metrics.program_expense_ratio,
      description: "Percentage of expenses spent on programs",
    },
    {
      label: "Fundraising Efficiency",
      value: metrics.fundraising_efficiency,
      description: "Fundraising costs as a share of total expenses",
    },
    {
      label: "Revenue Growth Rate",
      value: metrics.revenue_growth_rate,
      description: "Year-over-year revenue growth",
    },
  ];

  return (
    <div data-testid="metrics-cards">
      <h2 className="mb-4 text-lg font-semibold">Key Metrics</h2>
      <div className="grid gap-4 sm:grid-cols-3">
        {items.map((item) => (
          <Card key={item.label}>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {item.label}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatPercent(item.value)}
              </div>
              <p className="mt-1 text-xs text-muted-foreground">
                {item.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
