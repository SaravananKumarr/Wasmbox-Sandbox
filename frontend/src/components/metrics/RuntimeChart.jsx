import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const runtimeData = [
  { time: "12:00", avgLatency: 16.2, p95Latency: 28.5 },
  { time: "13:00", avgLatency: 18.4, p95Latency: 31.0 },
  { time: "14:00", avgLatency: 15.1, p95Latency: 24.2 },
  { time: "15:00", avgLatency: 21.3, p95Latency: 38.9 },
  { time: "16:00", avgLatency: 17.8, p95Latency: 29.1 },
  { time: "17:00", avgLatency: 19.5, p95Latency: 32.4 },
  { time: "18:00", avgLatency: 14.8, p95Latency: 22.8 },
];

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;

  return (
    <div className="rounded-xl border border-blue-100 bg-white px-4 py-3 shadow-sm shadow-slate-200">
      <p className="text-xs text-slate-500">Time: {label}</p>
      <div className="mt-1 space-y-1">
        <p className="text-sm font-semibold text-slate-900">
          Avg Runtime: {payload[0]?.value} ms
        </p>
        {payload[1] && (
          <p className="text-xs text-slate-600">
            p95 Latency: {payload[1]?.value} ms
          </p>
        )}
      </div>
    </div>
  );
}

function RuntimeChart() {
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
