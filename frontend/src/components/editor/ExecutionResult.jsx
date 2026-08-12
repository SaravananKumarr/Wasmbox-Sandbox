import { Clock, Cpu, CheckCircle2, XCircle, Sliders, ShieldCheck, Gauge } from "lucide-react";
import Badge from "../common/Badge";

function ExecutionResult({ result, status = "idle", inputPayload, onInputPayloadChange }) {
  const usage = result?.resource_usage ?? {};
  const limits = result?.resource_limits ?? {};
  const duration = usage.duration_ms ?? result?.duration ?? null;
  const memory = usage.memory_mb ?? result?.memory ?? null;
  const fuel = usage.fuel_consumed;
  const exitCode = result?.returnCode ?? result?.return_code;
  const formatValue = (value, unit = "") => (value === null || value === undefined ? "Not available" : `${value}${unit}`);

  return (
    <div className="flex h-full flex-col space-y-4">
      {/* Test Input Payload Section */}
      <div className="flex flex-col rounded-xl border border-blue-100 bg-slate-50 p-4 shadow-sm">
        <div className="mb-2 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sliders className="h-4 w-4 text-sky-600" />
            <span className="text-xs font-semibold text-slate-700">Input Payload (JSON)</span>
          </div>
          <span className="text-[10px] text-slate-500">Passed to plugin entrypoint</span>
        </div>
        <textarea
          value={inputPayload}
          onChange={(e) => onInputPayloadChange && onInputPayloadChange(e.target.value)}
          rows={5}
          className="w-full resize-none rounded-lg border border-blue-100 bg-white p-3 font-mono text-xs text-slate-900 outline-none transition focus:border-sky-300/70"
          placeholder='{"key": "value"}'
        />
      </div>

      {/* Execution Stats Card */}
      <div className="flex flex-1 flex-col rounded-xl border border-blue-100 bg-slate-50 p-4 shadow-sm">
        <div className="mb-4 flex items-center justify-between border-b border-blue-100/80 pb-3">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-sky-600" />
            <span className="text-xs font-semibold text-slate-700">Sandbox Execution Metrics</span>
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
            <div className="grid grid-cols-2 gap-3 xl:grid-cols-4">
              <div className="rounded-lg border border-blue-100/90 bg-white p-2.5">
                <div className="flex items-center gap-1.5 text-xs text-slate-500">
                  <Clock className="h-3.5 w-3.5 text-sky-600" /> Latency
                </div>
                <p className="mt-1 font-mono text-sm font-semibold text-slate-900">
                  {formatValue(duration, " ms")}
                </p>
              </div>

              <div className="rounded-lg border border-blue-100/90 bg-white p-2.5">
                <div className="flex items-center gap-1.5 text-xs text-slate-500">
                  <Cpu className="h-3.5 w-3.5 text-sky-600" /> Memory
                </div>
                <p className="mt-1 font-mono text-sm font-semibold text-slate-900">
                  {formatValue(memory, " MB")}
                </p>
              </div>

              <div className="rounded-lg border border-blue-100/90 bg-white p-2.5">
                <div className="flex items-center gap-1.5 text-xs text-slate-500">
                  <Gauge className="h-3.5 w-3.5 text-sky-600" /> Fuel
                </div>
                <p className="mt-1 font-mono text-sm font-semibold text-slate-900">
                  {formatValue(fuel)}
                </p>
              </div>

              <div className="rounded-lg border border-blue-100/90 bg-white p-2.5">
                <div className="flex items-center gap-1.5 text-xs text-slate-500">
                  Exit Code
                </div>
                <p className={`mt-1 font-mono text-sm font-semibold ${exitCode === 0 ? "text-emerald-600" : "text-red-600"}`}>
                  {formatValue(exitCode)}
                </p>
              </div>
            </div>

            <div className="rounded-lg border border-blue-100 bg-white p-3">
              <p className="text-xs font-semibold text-slate-700">Active sandbox limits</p>
              <div className="mt-2 grid grid-cols-2 gap-x-3 gap-y-1 font-mono text-[11px] text-slate-600">
                <span>Timeout: {formatValue(limits.execution_timeout_ms, " ms")}</span>
                <span>Sandbox memory: {formatValue(limits.sandbox_memory_mb, " MB")}</span>
                <span>Wasm memory: {formatValue(limits.wasm_memory_mb, " MB")}</span>
                <span>Wasm fuel: {formatValue(limits.wasm_fuel)}</span>
              </div>
            </div>

            {result.error_message && (
              <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-xs text-red-700">
                <span className="font-semibold">Execution failed: </span>{result.error_message}
              </div>
            )}

            <div>
              <p className="mb-1 text-xs text-slate-500">Return Payload</p>
              <pre className="max-h-48 overflow-y-auto rounded-lg border border-blue-100 bg-slate-100 p-3 font-mono text-xs text-slate-900">
                {result.output}
              </pre>
            </div>
          </div>
        ) : (
          <div className="flex flex-1 items-center justify-center text-center text-xs text-slate-500">
            Execute the plugin to inspect runtime usage, active sandbox limits, and the response payload.
          </div>
        )}
      </div>
    </div>
  );
}

export default ExecutionResult;
