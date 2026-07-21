import React, { useState } from 'react';
import EditorComponent from '../components/Editor';

export default function Editor() {
  const [code, setCode] = useState('');
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Plugin Editor (Monaco IDE)</h1>
      <EditorComponent value={code} onChange={(e) => setCode(e.target.value)} />
    </div>
  );
}
