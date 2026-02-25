import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/format";
import type { Filing } from "@/lib/types";

interface FinancialOverviewProps {
  filing: Filing;
}

export function FinancialOverview({ filing }: FinancialOverviewProps) {
  const items = [
    { label: "Total Revenue", value: filing.total_revenue },
    { label: "Total Expenses", value: filing.total_expenses },
    { label: "Net Assets", value: filing.net_assets },
    {
      label: "Contributions & Grants",
      value: filing.contributions_and_grants,
    },
    { label: "Program Service Revenue", value: filing.program_service_revenue },
    { label: "Investment Income", value: filing.investment_income },
  ];

  return (
    <div data-testid="financial-overview">
      <h2 className="mb-4 text-lg font-semibold">
        Financial Overview ({filing.tax_year})
      </h2>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => (
          <Card key={item.label}>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {item.label}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-xl font-bold">
                {formatCurrency(item.value)}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
