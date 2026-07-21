import React from 'react';

export default function PluginList({ plugins }) {
  return (
    <ul>
      {plugins.map((p) => (
        <li key={p.id} className="border-b py-2">{p.name}</li>
      ))}
    </ul>
  );
}
