import time
from app.core.logger import logger


class FuelGuard:
    MAX_FUEL = 1_000_000

    @classmethod
    def enforce(cls, instance, max_fuel: int = MAX_FUEL):
        logger.info(f"Fuel guard enforced: max {max_fuel} units")
        # Wasmtime fuel metering
        instance.store.add_fuel(max_fuel)
        return max_fuel

    @classmethod
    def get_consumed(cls, instance) -> int:
        try:
            fuel_remaining = instance.store.get_fuel()
            return cls.MAX_FUEL - fuel_remaining
        except Exception:
            return 0
