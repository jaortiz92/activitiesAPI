from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Entorno
    ENV: str
    PROJECT_NAME: str = "ActivityV3"

    # Configuración de base de datos
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
