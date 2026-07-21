from app.sandbox.engine import SandboxEngine
from app.sandbox.linker import SandboxLinker


def test_engine_init():
    engine = SandboxEngine()
    assert engine.engine is not None


def test_linker_init():
    linker = SandboxLinker()
    allowed = linker.register_host_functions()
    assert "write_log" in allowed
