import React, { useState, useEffect } from 'react';

export default function useExecution() {
  const [result, setResult] = useState(null);
  return { result, setResult };
}
