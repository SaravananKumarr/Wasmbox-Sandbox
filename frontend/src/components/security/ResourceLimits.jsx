import { Sliders } from "lucide-react";
import { Card, CardContent, CardHeader } from "../common/Card";
import Badge from "../common/Badge";

function ResourceLimits({ policy }) {
  const limits = [{ label: "Memory limit", value: policy ? `${policy.memoryLimitMb} MB` : "--" }, { label: "CPU limit", value: policy ? `${policy.cpuLimitSeconds} s` : "--" }, { label: "Wall-clock timeout", value: policy ? `${policy.timeoutSeconds} s` : "--" }];
  return <Card><CardHeader><div className="flex items-center gap-3"><div className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-800 bg-slate-900 text-cyan-400"><Sliders className="h-4 w-4" /></div><div><h3 className="font-semibold text-slate-100">Resource Limits</h3><p className="text-xs text-slate-500">Configured through the backend environment; changes require a restart.</p></div></div></CardHeader><CardContent><div className="grid gap-4 md:grid-cols-3">{limits.map((limit) => <div key={limit.label} className="rounded-xl border border-slate-800 bg-[#0d111c] p-4"><p className="text-xs text-slate-500">{limit.label}</p><Badge variant="info" className="mt-3">{limit.value}</Badge></div>)}</div></CardContent></Card>;
}

export default ResourceLimits;
