export function connectWebSocket(url) {
  const ws = new WebSocket(url);
  return ws;
}
