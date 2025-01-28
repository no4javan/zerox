
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    TEMP_DIR: str = "/tmp/zerox"
    MAX_CONCURRENCY: int = 10
    CLEANUP_TEMP: bool = True

settings = Settings()

# models.py
from pydantic import BaseModel

class ConversionRequest(BaseModel):
    api_key: str
