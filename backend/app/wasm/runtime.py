from wasmtime import Config, Engine, Instance, Module, Store, wat2wasm


TRUSTED_SELF_CHECK_MODULE = """
(module
  (func (export \"add\") (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.add))
"""


def run_trusted_self_check() -> dict:
    """Exercise the embedded Wasmtime runtime with fuel metering enabled.

    This intentionally accepts no user code; it validates the runtime plumbing
    only and prevents the application from claiming a compiler is available.
    """
    config = Config()
    config.consume_fuel = True
    engine = Engine(config)
    module = Module(engine, wat2wasm(TRUSTED_SELF_CHECK_MODULE))
    store = Store(engine)
    store.set_fuel(10_000)
    instance = Instance(store, module, [])
    add = instance.exports(store)["add"]
    result = add(store, 20, 22)
    return {"runtime": "wasmtime", "fuelEnabled": True, "result": result}
