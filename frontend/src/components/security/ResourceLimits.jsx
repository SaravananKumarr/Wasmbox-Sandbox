import { useState } from "react";
import { Sliders, Save, Check } from "lucide-react";
import { Card, CardContent, CardHeader } from "../common/Card";
import Button from "../common/Button";
import Badge from "../common/Badge";

function ResourceLimits() {
  const [memoryLimit, setMemoryLimit] = useState(128);
  const [timeoutMs, setTimeoutMs] = useState(500);
  const [fuelBudget, setFuelBudget] = useState(5000000);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-blue-100 bg-sky-50 text-sky-700">
              <Sliders className="h-4 w-4" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900">Sandbox Resource Quotas</h3>
              <p className="text-xs text-slate-500">Prevent runaway scripts and DOS attacks via strict resource budgets.</p>
            </div>
          </div>

          <Button
            variant={saved ? "secondary" : "primary"}
            size="sm"
            icon={saved ? Check : Save}
            onClick={handleSave}
          >
            {saved ? "Quotas Saved" : "Save Quotas"}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid gap-6 md:grid-cols-3">
          {/* Memory limit slider */}
          <div className="rounded-xl border border-blue-100 bg-white p-4 shadow-sm shadow-slate-100">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-700">Max Linear Memory</span>
              <Badge variant="info">{memoryLimit} MB</Badge>
            </div>
            <p className="mt-1 text-[11px] text-slate-500">Maximum heap RAM granted to guest WASM instance.</p>
            <input
              type="range"
              min="32"
              max="512"
              step="32"
              value={memoryLimit}
              onChange={(e) => setMemoryLimit(Number(e.target.value))}
              className="mt-4 w-full accent-sky-500 cursor-pointer"
            />
            <div className="mt-1 flex justify-between text-[10px] text-slate-500">
              <span>32 MB</span>
              <span>256 MB</span>
              <span>512 MB</span>
            </div>
          </div>

          {/* Execution Timeout slider */}
          <div className="rounded-xl border border-blue-100 bg-white p-4 shadow-sm shadow-slate-100">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-700">Execution Timeout</span>
              <Badge variant="warning">{timeoutMs} ms</Badge>
            </div>
            <p className="mt-1 text-[11px] text-slate-500">Hard CPU time wall limit for single function calls.</p>
            <input
              type="range"
              min="100"
              max="2000"
              step="100"
              value={timeoutMs}
              onChange={(e) => setTimeoutMs(Number(e.target.value))}
              className="mt-4 w-full accent-amber-500 cursor-pointer"
            />
            <div className="mt-1 flex justify-between text-[10px] text-slate-500">
              <span>100 ms</span>
              <span>1000 ms</span>
              <span>2000 ms</span>
            </div>
          </div>

          {/* Wasm Fuel Limit */}
          <div className="rounded-xl border border-blue-100 bg-white p-4 shadow-sm shadow-slate-100">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-700">Wasm Instruction Fuel</span>
              <Badge variant="neutral">{(fuelBudget / 1000000).toFixed(1)}M units</Badge>
            </div>
            <p className="mt-1 text-[11px] text-slate-500">Deterministic WebAssembly instruction opcode counter budget.</p>
            <input
              type="range"
              min="1000000"
              max="20000000"
              step="1000000"
              value={fuelBudget}
              onChange={(e) => setFuelBudget(Number(e.target.value))}
              className="mt-4 w-full accent-cyan-500 cursor-pointer"
            />
            <div className="mt-1 flex justify-between text-[10px] text-slate-500">
              <span>1M</span>
              <span>10M</span>
              <span>20M</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default ResourceLimits;
