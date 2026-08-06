import { ShieldCheck, Cpu, Lock, CheckCircle2 } from "lucide-react";
import Badge from "../common/Badge";
import { Card, CardContent, CardHeader } from "../common/Card";

function SandboxStatus() {
  return (
    <Card className="border-emerald-500/20 bg-white">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900">Sandbox Isolation Engine</h3>
              <p className="text-xs text-slate-600">Strict WebAssembly memory isolation active</p>
            </div>
          </div>
          <Badge variant="success" className="gap-1.5 px-3 py-1 text-xs">
            <CheckCircle2 className="h-3.5 w-3.5" /> Enforcing Policy
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 pt-2">
          <div className="rounded-xl border border-blue-100 bg-slate-50 p-4">
            <div className="flex items-center gap-2 text-xs text-slate-600">
              <Cpu className="h-4 w-4 text-violet-400" /> Runtime Engine
            </div>
            <p className="mt-2 font-mono text-sm font-semibold text-slate-900">Wasmtime v46.0</p>
            <p className="mt-0.5 text-[11px] text-slate-600">JIT / Compiler isolate</p>
          </div>

          <div className="rounded-xl border border-blue-100 bg-slate-50 p-4">
            <div className="flex items-center gap-2 text-xs text-slate-600">
              <Lock className="h-4 w-4 text-emerald-400" /> Memory Bounds
            </div>
            <p className="mt-2 font-mono text-sm font-semibold text-slate-900">Guard Pages (4GB)</p>
            <p className="mt-0.5 text-[11px] text-slate-600">Linear memory sandboxing</p>
          </div>

          <div className="rounded-xl border border-blue-100 bg-slate-50 p-4">
            <div className="flex items-center gap-2 text-xs text-slate-600">
              <ShieldCheck className="h-4 w-4 text-cyan-400" /> WASI Capabilities
            </div>
            <p className="mt-2 font-mono text-sm font-semibold text-slate-900">Capability-Based</p>
            <p className="mt-0.5 text-[11px] text-slate-600">Explicit handle grants only</p>
          </div>

          <div className="rounded-xl border border-blue-100 bg-slate-50 p-4">
            <div className="flex items-center gap-2 text-xs text-slate-600">
              <CheckCircle2 className="h-4 w-4 text-amber-400" /> Audit Log Engine
            </div>
            <p className="mt-2 font-mono text-sm font-semibold text-slate-900">Immutable</p>
            <p className="mt-0.5 text-[11px] text-slate-600">100% violation capture</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default SandboxStatus;
