import React from 'react';

export default function Metrics({ memory, fuel, time }) {
  return (
    <div className="flex gap-4">
      <div className="bg-blue-100 p-3 rounded">Memory: {memory} bytes</div>
      <div className="bg-green-100 p-3 rounded">Fuel: {fuel}</div>
      <div className="bg-yellow-100 p-3 rounded">Time: {time}ms</div>
    </div>
  );
}
