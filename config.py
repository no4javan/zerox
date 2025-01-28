
from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TEMP_DIR: str = "/tmp/zerox"
    MAX_CONCURRENCY: int = 10
    CLEANUP_TEMP: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
