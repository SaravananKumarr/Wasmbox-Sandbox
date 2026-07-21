import React, { useState } from 'react';

export default function useMetrics() {
  const [metrics, setMetrics] = useState({ memory: 0, fuel: 0, time: 0 });
  return { metrics, setMetrics };
}
