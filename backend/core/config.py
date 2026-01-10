"""
Конфигурация приложения
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    PROJECT_NAME: str = "BAL_BUS"
    DEBUG: bool = True
    
    # База данных (по умолчанию SQLite для простоты)
    DATABASE_URL: str = "sqlite+aiosqlite:///./balbus.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email настройки (для отправки билетов)
    SMTP_ENABLED: bool = False  # Включить реальную отправку email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""  # Email отправителя
    SMTP_PASSWORD: str = ""  # Пароль или токен приложения
    SMTP_FROM_NAME: str = "BAL_BUS"  # Имя отправителя
    SMTP_USE_TLS: bool = True  # Использовать TLS (для порта 587)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

