import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

function buildStatusData(history) {
  const successful = history.filter((item) => item.status === "Success").length;
  const failed = history.length - successful;
  return [
    { name: "Successful Runs", value: successful, color: "#10b981" },
    { name: "Failed Runs", value: failed, color: "#ef4444" },
  ].filter((item) => item.value > 0);
}

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const item = payload[0];

  return (
    <div className="rounded-xl border border-slate-700 bg-[#0d111c] px-4 py-3 shadow-xl">
      <p className="text-xs text-slate-500">{item.name}</p>
      <p className="mt-1 text-sm font-semibold text-slate-100">
        {item.value} runs ({(item.value / 12.84).toFixed(1)}%)
      </p>
    </div>
  );
}

function SuccessRateChart({ history = [] }) {
  const data = buildStatusData(history);
  return (
    <div className="h-[280px] w-full flex items-center justify-center">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="45%"
            innerRadius={60}
            outerRadius={85}
            paddingAngle={4}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} stroke="#070912" strokeWidth={2} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            verticalAlign="bottom"
            height={36}
            formatter={(value) => <span className="text-xs text-slate-300 ml-1">{value}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default SuccessRateChart;
