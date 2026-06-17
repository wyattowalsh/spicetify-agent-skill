type RiskLevel = "read" | "medium" | "high" | "blocked";

export function RiskBadge({ level, label }: { level: RiskLevel; label: string }) {
  return <div className={`risk-badge risk-${level}`}>{label}</div>;
}
