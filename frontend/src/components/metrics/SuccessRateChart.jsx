import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

const data = [
  { name: "Successful Runs", value: 1267, color: "#10b981" },
  { name: "Runtime Failures", value: 14, color: "#ef4444" },
  { name: "Policy Violations", value: 3, color: "#f59e0b" },
];

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const item = payload[0];

  return (
    <div className="rounded-xl border border-blue-100 bg-white px-4 py-3 shadow-sm shadow-slate-200">
      <p className="text-xs text-slate-600">{item.name}</p>
      <p className="mt-1 text-sm font-semibold text-slate-900">
        {item.value} runs ({(item.value / 12.84).toFixed(1)}%)
      </p>
    </div>
  );
}

function SuccessRateChart() {
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
            formatter={(value) => <span className="text-xs text-slate-600 ml-1">{value}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default SuccessRateChart;
