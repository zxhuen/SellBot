from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    DATABASE_URL: str
    DATABASE_PASSWORD: str
    GEMINI_API_KEY: str
    REDIS_KEY: str
    ASYNC_DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
