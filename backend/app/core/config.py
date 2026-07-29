import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    APP_NAME = os.getenv("APP_NAME", "WasmBox Sandbox")

    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

    DEBUG = os.getenv("DEBUG", "true").lower() == "true"

    HOST = os.getenv("HOST", "0.0.0.0")

    PORT = int(os.getenv("PORT", "8000"))

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/wasmbox_db"
    )

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

    ALGORITHM = os.getenv("ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # Plugin storage
    PLUGIN_STORAGE_DIR = os.getenv("PLUGIN_STORAGE_DIR", "storage/plugins")

    MAX_PLUGIN_SIZE_MB = int(os.getenv("MAX_PLUGIN_SIZE_MB", "10"))

    # WASM execution sandbox limits
    WASM_FUEL_LIMIT = int(os.getenv("WASM_FUEL_LIMIT", "10000000"))

    WASM_MAX_MEMORY_MB = int(os.getenv("WASM_MAX_MEMORY_MB", "64"))

    WASM_TIMEOUT_SECONDS = float(os.getenv("WASM_TIMEOUT_SECONDS", "5"))


settings = Settings()
