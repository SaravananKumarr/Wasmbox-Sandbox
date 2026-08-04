import { ShieldAlert, Cpu, Lock, CheckCircle2 } from "lucide-react";
import Badge from "../common/Badge";
import { Card, CardContent, CardHeader } from "../common/Card";

function SandboxStatus({ policy }) {
  const runtime = policy?.runtime || "Loading policy...";
  return (
    <Card className="border-amber-500/20 bg-gradient-to-br from-[#0d111c] via-[#090c15] to-[#0b1322]">
      <CardHeader><div className="flex items-center justify-between"><div className="flex items-center gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-xl border border-amber-500/20 bg-amber-500/10 text-amber-400"><ShieldAlert className="h-6 w-6" /></div><div><h3 className="font-semibold text-slate-100">Sandbox Policy</h3><p className="text-xs text-slate-400">Live backend configuration</p></div></div><Badge variant="warning" className="gap-1.5 px-3 py-1 text-xs"><CheckCircle2 className="h-3.5 w-3.5" /> {policy?.mode || "Loading"}</Badge></div></CardHeader>
      <CardContent><div className="grid gap-4 pt-2 sm:grid-cols-2 lg:grid-cols-4"><div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4"><div className="flex items-center gap-2 text-xs text-slate-500"><Cpu className="h-4 w-4 text-violet-400" /> Plugin runtime</div><p className="mt-2 text-sm font-semibold text-slate-100">{runtime}</p></div><div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4"><div className="flex items-center gap-2 text-xs text-slate-500"><Cpu className="h-4 w-4 text-emerald-400" /> WASM foundation</div><p className="mt-2 text-sm font-semibold text-slate-100">{policy?.wasmRuntime || "--"}</p></div><div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4"><div className="flex items-center gap-2 text-xs text-slate-500"><Lock className="h-4 w-4 text-cyan-400" /> Memory cap</div><p className="mt-2 font-mono text-sm font-semibold text-slate-100">{policy ? `${policy.memoryLimitMb} MB` : "--"}</p></div><div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4"><div className="flex items-center gap-2 text-xs text-slate-500"><CheckCircle2 className="h-4 w-4 text-amber-400" /> Python compiler</div><p className="mt-2 font-mono text-sm font-semibold text-slate-100">{policy ? (policy.pythonCompilerAvailable ? "Available" : "Not available") : "--"}</p></div></div>{policy?.notice && <p className="mt-4 rounded-lg border border-amber-500/20 bg-amber-500/5 px-3 py-2 text-xs leading-5 text-amber-200">{policy.notice}</p>}</CardContent>
    </Card>
  );
}

export default SandboxStatus;
