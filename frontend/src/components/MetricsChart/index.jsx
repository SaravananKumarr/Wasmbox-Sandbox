import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

export default function MetricsChart({ data }) {
  const chartData = data || [
    { name: 'Run 1', memory: 1024, fuel: 500 },
    { name: 'Run 2', memory: 2048, fuel: 750 },
  ];
  return (
    <div className="p-4 bg-white rounded shadow">
      <h3 className="font-bold mb-2">Execution Metrics</h3>
      <LineChart width={400} height={200} data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="memory" stroke="#8884d8" />
        <Line type="monotone" dataKey="fuel" stroke="#82ca9d" />
      </LineChart>
    </div>
  );
}
