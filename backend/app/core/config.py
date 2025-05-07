from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_URL: str = "postgresql+asyncpg://user:password@postgres/car_db"
    REDIS_URL: str = "redis://redis:6379"
    
    class Config:
        env_file = ".env"

settings = Settings()