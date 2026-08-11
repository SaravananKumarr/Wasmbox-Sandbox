from dataclasses import dataclass

from wasmtime import Config, Engine, Instance, Module, Store, Trap, WasmtimeError

from app.core.config import settings


@dataclass
class WasmExecutionResult:
    status: str
    fuel_consumed: int
    error: str | None = None
    return_value: object | None = None


class WasmRuntime:
    """Creates Wasmtime stores with a fixed fuel budget per execution."""

    def __init__(
        self,
        fuel_limit: int | None = None,
        memory_limit_bytes: int | None = None,
    ):
        self.fuel_limit = fuel_limit or settings.WASM_FUEL_LIMIT
        if self.fuel_limit <= 0:
            raise ValueError("fuel_limit must be greater than zero")

        self.memory_limit_bytes = memory_limit_bytes or (
            settings.WASM_MEMORY_LIMIT_MB * 1024 * 1024
        )
        if self.memory_limit_bytes <= 0:
            raise ValueError("memory_limit_bytes must be greater than zero")

        config = Config()
        config.consume_fuel = True
        self.engine = Engine(config)

    def create_store(self) -> Store:
        store = Store(self.engine)
        store.set_fuel(self.fuel_limit)
        store.set_limits(memory_size=self.memory_limit_bytes)
        return store

    def run_wat(self, wat_source: str, export_name: str = "run") -> WasmExecutionResult:
        """Run a trusted WAT fixture and report fuel usage for runtime tests."""
        store = self.create_store()
        try:
            module = Module(self.engine, wat_source)
            instance = Instance(store, module, [])
            exported_function = instance.exports(store)[export_name]
            return_value = exported_function(store)
            return WasmExecutionResult(
                status="Success",
                fuel_consumed=self.fuel_limit - store.get_fuel(),
                return_value=return_value,
            )
        except (Trap, WasmtimeError) as exc:
            fuel_consumed = self.fuel_limit - store.get_fuel()
            status = "FuelExhausted" if store.get_fuel() == 0 else "Failed"
            return WasmExecutionResult(
                status=status,
                fuel_consumed=fuel_consumed,
                error=str(exc),
            )


runtime = WasmRuntime()
