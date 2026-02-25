import { Badge } from "@/components/ui/badge";
import type { OrganizationProfile } from "@/lib/types";

interface ProfileHeaderProps {
  org: OrganizationProfile;
}

export function ProfileHeader({ org }: ProfileHeaderProps) {
  const latestFiling = org.filings[0];

  return (
    <div data-testid="profile-header">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">{org.name}</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            EIN: {org.ein}
            {org.city && org.state ? ` | ${org.city}, ${org.state}` : ""}
            {org.ruling_date ? ` | Ruling Date: ${org.ruling_date}` : ""}
          </p>
        </div>
        {org.ntee_code && (
          <Badge variant="secondary" className="text-sm">
            {org.ntee_code}
          </Badge>
        )}
      </div>
      {latestFiling?.mission_description && (
        <p className="mt-4 text-sm leading-relaxed text-muted-foreground">
          {latestFiling.mission_description}
        </p>
      )}
    </div>
  );
}
