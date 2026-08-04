import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function buildActivityData(history) {
  const days = Array.from({ length: 7 }, (_, index) => {
    const date = new Date();
    date.setDate(date.getDate() - (6 - index));
    return { key: date.toDateString(), day: date.toLocaleDateString(undefined, { weekday: "short" }), executions: 0 };
  });
  history.forEach((item) => {
    const executedAt = new Date(item.createdAt);
    const match = days.find((day) => day.key === executedAt.toDateString());
    if (match) match.executions += 1;
  });
  return days;
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;

  return (
    <div className="rounded-xl border border-slate-700 bg-[#0d111c] px-4 py-3 shadow-xl">
      <p className="text-xs text-slate-500">{label}</p>

      <p className="mt-1 text-sm font-semibold text-slate-100">
        {payload[0].value} executions
      </p>
    </div>
  );
}

function ActivityChart({ history = [] }) {
  const data = buildActivityData(history);
  return (
    <div className="h-[280px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={data}
          margin={{
            top: 15,
            right: 10,
            left: -15,
            bottom: 0,
          }}
        >
          <defs>
            <linearGradient
              id="executionGradient"
              x1="0"
              y1="0"
              x2="0"
              y2="1"
            >
              <stop
                offset="5%"
                stopColor="#8b5cf6"
                stopOpacity={0.35}
              />

              <stop
                offset="95%"
                stopColor="#8b5cf6"
                stopOpacity={0}
              />
            </linearGradient>
          </defs>

          <CartesianGrid
            strokeDasharray="4 4"
            vertical={false}
            stroke="#1e293b"
          />

          <XAxis
            dataKey="day"
            axisLine={false}
            tickLine={false}
            tick={{
              fill: "#64748b",
              fontSize: 12,
            }}
            dy={10}
          />

          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{
              fill: "#64748b",
              fontSize: 12,
            }}
          />

          <Tooltip
            content={<CustomTooltip />}
            cursor={{
              stroke: "#475569",
              strokeDasharray: "4 4",
            }}
          />

          <Area
            type="monotone"
            dataKey="executions"
            stroke="#8b5cf6"
            strokeWidth={3}
            fill="url(#executionGradient)"
            activeDot={{
              r: 6,
              fill: "#8b5cf6",
              stroke: "#c4b5fd",
              strokeWidth: 2,
            }}
            animationDuration={1000}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ActivityChart;
