from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_URL: str = "postgresql+asyncpg://user:password@postgres/car_db"
    REDIS_URL: str = "redis://redis:6379"
    LLM_TYPE: str = "gpt-4"
    OPENAI_API_KEY: str = ""
    RAG_DB_PATH: str = "rag_vectorstore/faiss_index"
    
    class Config:
        env_file = ".env"

# Instantiate settings directly
settings = Settings()