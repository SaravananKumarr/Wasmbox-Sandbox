import React from 'react';

export default function Toast({ message }) {
  return (
    <div className="fixed bottom-4 right-4 bg-green-600 text-white p-3 rounded shadow-lg">
      {message}
    </div>
  );
}
