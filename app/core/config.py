from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Bot
    bot_token: str
    operator_chat_id: int
    
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str
    postgres_db: str = "model_agency"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Payment
    usdt_wallet: str = "TYourWalletAddressHere"  # 🔥 Значение по умолчанию
    
    # Optional
    trongrid_api_key: Optional[str] = None
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"  # Игнорировать лишние переменные в .env
    )

# Создаем единственный экземпляр настроек
settings = Settings()

# 🔥 Не нужно дублировать переменные! Используй settings.USDT_WALLET