import os

import dotenv

dotenv.load_dotenv()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Congress Info API")
    API_V1_STR: str = "/api/v1"
    all_cors_origins: list[str] = [
        origin.strip()
        for origin in os.getenv("BACKEND_CORS_ORIGINS", "").split(",")
        if origin.strip()
    ]

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        user = os.getenv("MYSQL_USER", "")
        password = os.getenv("MYSQL_PASSWORD", "")
        host = os.getenv("MYSQL_SERVER", "")
        port = os.getenv("MYSQL_PORT", "3306")
        database = os.getenv("MYSQL_DB", "")
        # For MariaDB 10.5+, use mariadb connector
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"

    FILE_UPLOAD_DIR: str = os.getenv("FILE_UPLOAD_DIR", "./files")

    # Email settings
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_TLS: bool = os.getenv("SMTP_TLS", "True").lower() == "true"
    SMTP_SSL: bool = os.getenv("SMTP_SSL", "False").lower() == "true"
    EMAILS_FROM_EMAIL: str = os.getenv("EMAILS_FROM_EMAIL", "info@dpl.at")
    EMAILS_FROM_NAME: str = os.getenv("PROJECT_NAME", "Congress Info API")

    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    class Config:
        case_sensitive = True


settings = Settings()
