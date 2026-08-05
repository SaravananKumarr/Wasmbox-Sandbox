import { ShieldCheck, Cpu, Lock, CheckCircle2 } from "lucide-react";
import Badge from "../common/Badge";
import { Card, CardContent, CardHeader } from "../common/Card";

function SandboxStatus() {
  return (
    <Card className="border-sky-100 bg-gradient-to-br from-white via-sky-50 to-slate-50">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-100 text-sky-700 border border-sky-200">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900">Sandbox Isolation Engine</h3>
              <p className="text-xs text-slate-500">Strict WebAssembly memory isolation active</p>
            </div>
          </div>
          <Badge variant="success" className="gap-1.5 px-3 py-1 text-xs">
            <CheckCircle2 className="h-3.5 w-3.5" /> Enforcing Policy
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 pt-2">
          <div className="rounded-xl border border-blue-100 bg-white p-4 shadow-sm shadow-slate-100">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <Cpu className="h-4 w-4 text-sky-600" /> Runtime Engine
            </div>
            <p className="mt-2 font-mono text-sm font-semibold text-slate-900">Wasmtime v46.0</p>
            <p className="mt-0.5 text-[11px] text-slate-500">JIT / Compiler isolate</p>
          </div>

          <div className="rounded-xl border border-blue-100 bg-white p-4 shadow-sm shadow-slate-100">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <Lock className="h-4 w-4 text-emerald-600" /> Memory Bounds
            </div>
            <p className="mt-2 font-mono text-sm font-semibold text-slate-900">Guard Pages (4GB)</p>
            <p className="mt-0.5 text-[11px] text-slate-500">Linear memory sandboxing</p>
          </div>

          <div className="rounded-xl border border-blue-100 bg-white p-4 shadow-sm shadow-slate-100">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <ShieldCheck className="h-4 w-4 text-cyan-600" /> WASI Capabilities
            </div>
            <p className="mt-2 font-mono text-sm font-semibold text-slate-900">Capability-Based</p>
            <p className="mt-0.5 text-[11px] text-slate-500">Explicit handle grants only</p>
          </div>

          <div className="rounded-xl border border-blue-100 bg-white p-4 shadow-sm shadow-slate-100">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <CheckCircle2 className="h-4 w-4 text-amber-500" /> Audit Log Engine
            </div>
            <p className="mt-2 font-mono text-sm font-semibold text-slate-900">Immutable</p>
            <p className="mt-0.5 text-[11px] text-slate-500">100% violation capture</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default SandboxStatus;
