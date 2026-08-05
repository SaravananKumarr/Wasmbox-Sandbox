import { Clock, Cpu, CheckCircle2, XCircle, Sliders, ShieldCheck } from "lucide-react";
import Badge from "../common/Badge";

function ExecutionResult({ result, status = "idle", inputPayload, onInputPayloadChange }) {
  return (
    <div className="flex h-full flex-col space-y-4">
      {/* Test Input Payload Section */}
      <div className="flex flex-col rounded-xl border border-slate-800 bg-[#0d111c] p-4 shadow-md">
        <div className="mb-2 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sliders className="h-4 w-4 text-violet-400" />
            <span className="text-xs font-semibold text-slate-200">Input Payload (JSON)</span>
          </div>
          <span className="text-[10px] text-slate-500">Passed to plugin entrypoint</span>
        </div>
        <textarea
          value={inputPayload}
          onChange={(e) => onInputPayloadChange && onInputPayloadChange(e.target.value)}
          rows={5}
          className="w-full resize-none rounded-lg border border-slate-800 bg-[#070912] p-3 font-mono text-xs text-slate-200 outline-none transition focus:border-violet-500/50"
          placeholder='{"key": "value"}'
        />
      </div>

      {/* Execution Stats Card */}
      <div className="flex flex-1 flex-col rounded-xl border border-slate-800 bg-[#0d111c] p-4 shadow-md">
        <div className="mb-4 flex items-center justify-between border-b border-slate-800/80 pb-3">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-emerald-400" />
            <span className="text-xs font-semibold text-slate-200">Sandbox Execution Metrics</span>
          </div>
          {status === "success" && (
            <Badge variant="success" className="gap-1">
              <CheckCircle2 className="h-3 w-3" /> Success
            </Badge>
          )}
          {status === "failed" && (
            <Badge variant="danger" className="gap-1">
              <XCircle className="h-3 w-3" /> Failed
            </Badge>
          )}
          {status === "running" && (
            <Badge variant="warning">Executing...</Badge>
          )}
          {status === "idle" && (
            <Badge variant="neutral">Idle</Badge>
          )}
        </div>

        {result ? (
          <div className="space-y-4">
            <div className="grid grid-cols-3 gap-3">
              <div className="rounded-lg border border-slate-800/80 bg-slate-900/60 p-2.5">
                <div className="flex items-center gap-1.5 text-xs text-slate-500">
                  <Clock className="h-3.5 w-3.5 text-cyan-400" /> Latency
                </div>
                <p className="mt-1 font-mono text-sm font-semibold text-slate-200">
                  {result.duration} ms
                </p>
              </div>

              <div className="rounded-lg border border-slate-800/80 bg-slate-900/60 p-2.5">
                <div className="flex items-center gap-1.5 text-xs text-slate-500">
                  <Cpu className="h-3.5 w-3.5 text-violet-400" /> Memory
                </div>
                <p className="mt-1 font-mono text-sm font-semibold text-slate-200">
                  {result.memory} MB
                </p>
              </div>

              <div className="rounded-lg border border-slate-800/80 bg-slate-900/60 p-2.5">
                <div className="flex items-center gap-1.5 text-xs text-slate-500">
                  Exit Code
                </div>
                <p className={`mt-1 font-mono text-sm font-semibold ${result.returnCode === 0 ? "text-emerald-400" : "text-red-400"}`}>
                  {result.returnCode}
                </p>
              </div>
            </div>

            <div>
              <p className="mb-1 text-xs text-slate-500">Return Payload</p>
              <pre className="max-h-48 overflow-y-auto rounded-lg border border-slate-800 bg-[#070912] p-3 font-mono text-xs text-slate-300">
                {result.output}
              </pre>
            </div>
          </div>
        ) : (
          <div className="flex flex-1 items-center justify-center text-center text-xs text-slate-500">
            Execute the plugin to inspect Wasmtime runtime duration, memory allocation, and response payloads.
          </div>
        )}
      </div>
    </div>
  );
}

export default ExecutionResult;
