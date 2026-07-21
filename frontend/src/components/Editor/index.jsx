import React from 'react';

export default function EditorComponent({ value, onChange }) {
  return (
    <textarea
      className="w-full h-96 p-4 border rounded-lg shadow-sm font-mono text-sm"
      value={value}
      onChange={onChange}
    />
  );
}
