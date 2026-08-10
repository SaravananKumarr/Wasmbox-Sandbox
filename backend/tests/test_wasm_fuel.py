import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.sandbox.runtime import WasmRuntime


def test_finite_wasm_function_reports_fuel_consumption():
    runtime = WasmRuntime(fuel_limit=100)

    result = runtime.run_wat('(module (func (export "run") nop nop))')

    assert result.status == "Success"
    assert 0 < result.fuel_consumed < 100
    assert result.error is None


def test_infinite_wasm_loop_exhausts_fuel():
    runtime = WasmRuntime(fuel_limit=100)

    result = runtime.run_wat('(module (func (export "run") (loop br 0)))')

    assert result.status == "FuelExhausted"
    assert result.fuel_consumed == 100
    assert result.error
