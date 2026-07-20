from fastapi import FastAPI

app = FastAPI(
    title="WasmBox Backend",
    version="1.0.0",
    description="Secure Multi-Tenant Plugin Sandbox"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to WasmBox Backend"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }