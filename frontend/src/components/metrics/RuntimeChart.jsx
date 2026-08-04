import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function buildRuntimeData(history) {
  return history.slice(0, 12).reverse().map((item, index) => ({
    time: item.timestamp || `Run ${index + 1}`,
    avgLatency: item.duration,
    p95Latency: item.duration,
  }));
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;

  return (
    <div className="rounded-xl border border-slate-700 bg-[#0d111c] px-4 py-3 shadow-xl">
      <p className="text-xs text-slate-500">Time: {label}</p>
      <div className="mt-1 space-y-1">
        <p className="text-sm font-semibold text-cyan-400">
          Avg Runtime: {payload[0]?.value} ms
        </p>
        {payload[1] && (
          <p className="text-xs text-violet-400">
            p95 Latency: {payload[1]?.value} ms
          </p>
        )}
      </div>
    </div>
  );
}

function RuntimeChart({ history = [] }) {
  const runtimeData = buildRuntimeData(history);
  return (
    <div className="h-[280px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={runtimeData}
          margin={{ top: 15, right: 10, left: -15, bottom: 0 }}
        >
          <defs>
            <linearGradient id="latencyGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="4 4" vertical={false} stroke="#1e293b" />
          <XAxis
            dataKey="time"
            axisLine={false}
            tickLine={false}
            tick={{ fill: "#64748b", fontSize: 12 }}
            dy={10}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{ fill: "#64748b", fontSize: 12 }}
            unit=" ms"
          />
          <Tooltip content={<CustomTooltip />} />
          <Area
            type="monotone"
            dataKey="avgLatency"
            stroke="#06b6d4"
            strokeWidth={3}
            fill="url(#latencyGradient)"
            activeDot={{ r: 6, fill: "#06b6d4", stroke: "#a5f3fc", strokeWidth: 2 }}
          />
          <Area
            type="monotone"
            dataKey="p95Latency"
            stroke="#8b5cf6"
            strokeWidth={2}
            strokeDasharray="4 4"
            fill="transparent"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RuntimeChart;
