from dotenv import load_dotenv
import os

load_dotenv()

class Settings:

    APP_NAME = os.getenv("APP_NAME")

    APP_VERSION = os.getenv("APP_VERSION")

    DEBUG = os.getenv("DEBUG")

    HOST = os.getenv("HOST")

    PORT = os.getenv("PORT")

    DATABASE_URL = os.getenv("DATABASE_URL")

    SECRET_KEY = os.getenv("SECRET_KEY")

    ALGORITHM = os.getenv("ALGORITHM")

    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://localhost:3000"
        ).split(",")
        if origin.strip()
    ]

    SANDBOX_TIMEOUT_SECONDS = float(os.getenv("SANDBOX_TIMEOUT_SECONDS", "8"))

    SANDBOX_CPU_SECONDS = int(os.getenv("SANDBOX_CPU_SECONDS", "5"))

    SANDBOX_MEMORY_MB = int(os.getenv("SANDBOX_MEMORY_MB", "128"))

settings = Settings()