import React, { createContext, useState } from 'react';

export const StoreContext = createContext();

export function StoreProvider({ children }) {
  const [plugins, setPlugins] = useState([]);
  return (
    <StoreContext.Provider value={{ plugins, setPlugins }}>
      {children}
    </StoreContext.Provider>
  );
}
