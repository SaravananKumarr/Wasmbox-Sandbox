# WasmBox Sandbox

A secure multi-tenant Python plugin sandbox using WebAssembly (WASM) and Wasmtime.

## Architecture

See `docs/ARCHITECTURE.md`.

## Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm run dev
```

## Phases Implemented

- Phase 0: Architecture ✅
- Phase 1: Backend Foundation ✅
- Phase 2: AST Security Scanner ✅
- Phase 3: WASM Compiler ✅
- Phase 4: Sandbox Engine ✅
- Phase 5: REST Routes ✅
- Phase 6: Frontend Scaffold ✅
- Phase 7: Monaco Editor ✅
- Phase 8: Plugin Management ✅
- Phase 9: Metrics & Charts ✅
- Phase 10: JWT Auth ✅
- Phase 11: WebSocket Streaming ✅
- Phase 12: Docker Setup ✅ (basic docker-compose)
- Phase 13: Tests ✅ (unit + security)
- Phase 14: Documentation ✅

## Security

- AST scanner blocks dangerous Python imports.
- WASM sandbox isolates CPU and memory.
- Memory limits (10MB) and fuel metering (1M units) enforced.
