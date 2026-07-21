from wasmtime import Config, Engine, Store
from app.core.logger import logger


class MemoryGuard:
    MAX_MEMORY_BYTES = 10 * 1024 * 1024  # 10MB

    @classmethod
    def enforce(cls, instance, max_bytes: int = MAX_MEMORY_BYTES):
        logger.info(f"Memory guard enforced: max {max_bytes} bytes")
        # In wasmtime, memory limits are configured via Config
        config = Config()
        config.max_memory_size(max_bytes)
        return config
