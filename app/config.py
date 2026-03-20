import os


class Settings:

    API_PORT = int(os.getenv("API_PORT", 8080))

    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_USER = os.getenv("DB_USER", "exporter")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")
    DB_NAME = os.getenv("DB_NAME", "exports_db")

    EXPORT_STORAGE_PATH = os.getenv("EXPORT_STORAGE_PATH", "/app/exports")


settings = Settings()