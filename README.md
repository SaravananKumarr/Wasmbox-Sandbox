# WasmBox

WasmBox is a local development MVP for creating, saving, and executing small Python plugins through a React developer portal. It records executions, exposes live metrics, and displays the active sandbox policy.

## Important security note

This repository currently runs plugins in a restricted Python subprocess with static source checks and timeout/resource limits. It **does not compile Python to WebAssembly** and is **not a production-grade isolation boundary**. Do not run untrusted code with this project outside an isolated development environment.

## Run locally

1. In `backend`, copy `.env.example` to `.env`, create a virtual environment, install `requirements.txt`, then run `python -m app.database.create_db` and `uvicorn main:app --reload --port 8000`.
2. In `frontend`, run `npm install` then `npm run dev`.
3. Open `http://localhost:5173`. The API documentation is at `http://localhost:8000/docs`.

## Verification

Run `pytest tests` from `backend`. Run `npm run lint` and `npm run build` from `frontend`.

## Containers

Run `docker compose up --build`, then open `http://localhost:8080`. The backend remains available at `http://localhost:8000`.

## Next production milestone

Replace the Python subprocess executor with a real WASM runtime and a reviewed compiler pipeline before claiming strong tenant isolation.
