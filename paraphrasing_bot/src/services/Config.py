import os


class Config:
    TZ = os.getenv("TZ", "America/Mexico_City")
    DEV_MODE = bool(os.getenv("DEV_MODE") != "false")
    APP_PORT = int(os.getenv("APP_PORT", 5000))
    APP_HOST = os.getenv("HOST", "0.0.0.0")

    BACKEND_ADDRESS = os.environ["BACKEND_ADDRESS"]

    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT = int(os.environ["POSTGRES_PORT"])
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]

    SQLALCHEMY_POOL_RECYCLE = int(os.getenv("SQLALCHEMY_POOL_RECYCLE", 90))
    SQLALCHEMY_POOL_TIMEOUT = int(os.getenv("SQLALCHEMY_POOL_TIMEOUT", 900))
    SQLALCHEMY_POOL_SIZE = int(os.getenv("SQLALCHEMY_POOL_SIZE", 200))
    SQLALCHEMY_POOL_MAX_OVERFLOW = int(os.getenv("SQLALCHEMY_POOL_MAX_OVERFLOW", 50))

    REDIS_HOST = os.environ["REDIS_HOST"]
    REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
    REDIS_PORT = int(os.environ["REDIS_PORT"])
    REDIS_DATABASE = os.environ["REDIS_DATABASE"]
    REDIS_DEFAULT_TTL = int(os.environ["REDIS_DEFAULT_TTL"])

    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
