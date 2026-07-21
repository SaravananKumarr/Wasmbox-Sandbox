import React, { useState, useEffect } from 'react';

export default function usePlugin() {
  const [plugins, setPlugins] = useState([]);
  useEffect(() => {
    // Mock fetch
  }, []);
  return { plugins };
}
