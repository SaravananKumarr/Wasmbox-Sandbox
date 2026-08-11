import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.sandbox.runtime import WasmRuntime


WASM_PAGE_BYTES = 64 * 1024


def test_memory_growth_is_denied_at_the_configured_limit():
    runtime = WasmRuntime(memory_limit_bytes=WASM_PAGE_BYTES)
    wat_source = """
        (module
          (memory 1)
          (func (export "run") (result i32)
            i32.const 1
            memory.grow))
    """

    result = runtime.run_wat(wat_source)

    assert result.status == "Success"
    # WebAssembly returns -1 when a requested memory.grow is denied.
    assert result.return_value == -1
