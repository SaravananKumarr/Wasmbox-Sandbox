from app.wasm.runtime import run_trusted_self_check


def test_trusted_wasm_runtime_self_check():
    result = run_trusted_self_check()
    assert result == {"runtime": "wasmtime", "fuelEnabled": True, "result": 42}
