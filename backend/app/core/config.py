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

settings = Settings()