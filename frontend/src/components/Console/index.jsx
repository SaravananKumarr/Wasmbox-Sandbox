import React from 'react';

export default function Console({ stdout, stderr }) {
  return (
    <div className="border rounded p-4 bg-black text-green-400 font-mono text-xs">
      <pre>{stdout}</pre>
      <pre className="text-red-400">{stderr}</pre>
    </div>
  );
}
