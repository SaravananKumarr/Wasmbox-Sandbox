import { HardDrive, Globe, Terminal, FileCode2 } from "lucide-react";
import { Card, CardContent, CardHeader } from "../common/Card";
import Badge from "../common/Badge";

function PermissionCard({ policy }) {
  const permissions = [{ title: "Filesystem access", enabled: policy?.filesystemAccess, icon: HardDrive }, { title: "Network access", enabled: policy?.networkAccess, icon: Globe }, { title: "Environment access", enabled: policy?.environmentAccess, icon: Terminal }, { title: "Host functions", enabled: policy?.hostFunctions, icon: FileCode2 }];
  return <Card><CardHeader><div><h3 className="font-semibold text-slate-100">Sandbox Capabilities</h3><p className="mt-1 text-sm text-slate-500">Read-only policy reported by the backend.</p></div></CardHeader><CardContent><div className="grid gap-4 md:grid-cols-2">{permissions.map((permission) => { const Icon = permission.icon; return <div key={permission.title} className="flex items-center justify-between gap-4 rounded-xl border border-slate-800 bg-[#0d111c] p-4"><div className="flex items-center gap-3"><div className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-800 bg-slate-900 text-violet-400"><Icon className="h-4 w-4" /></div><h4 className="text-sm font-semibold text-slate-200">{permission.title}</h4></div><Badge variant={permission.enabled ? "success" : "danger"}>{policy ? (permission.enabled ? "Allowed" : "Denied") : "Loading"}</Badge></div>; })}</div></CardContent></Card>;
}

export default PermissionCard;
