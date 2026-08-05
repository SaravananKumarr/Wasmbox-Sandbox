from wasmtime import Engine, Store


class WasmRuntime:
    """
    Creates a reusable Wasmtime engine and store.
    """

    def __init__(self):
        self.engine = Engine()

    def create_store(self):
        return Store(self.engine)


runtime = WasmRuntime()