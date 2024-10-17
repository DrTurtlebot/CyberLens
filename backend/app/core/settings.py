# Script to run to boot web server "uvicorn main:app --host 127.0.0.1 --port 80 --reload", also "npm run serve"
from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import List


# Load Settings
class Settings(BaseSettings):
    ENV_API_PROXYCHECK_KEY: str
    ENV_API_PROXYCHECK_URL: str
    ENV_API_ABUSEIPDB_KEY: str
    ENV_API_ABUSEIPDB_URL: str
    ENV_API_VIRUSTOTAL_KEY: str
    ENV_API_URLSCAN_KEY: str
    ENV_API_URLSCAN_URL: str
    ENV_API_WHODAT_URL: str
    ENV_CACHE_RETENTION_HOURS: int
    ENV_API_OPENAI_KEY: str
    ENV_MONGO_URI: str
    LOGFIRE_TOKEN: str
    PRODUCTION: bool = False
    ENV_CORS_WHITELIST: str = Field(
        ..., description="Comma-separated list of CORS whitelist URLs"
    )

    @field_validator("ENV_CORS_WHITELIST", mode="after")
    def split_cors_whitelist(cls, value: str) -> List[str]:
        # If the value is a string, split it by commas and strip whitespace
        if isinstance(value, str):
            return [url.strip() for url in value.split(",")]
        # If the value is already a list (for some reason), return it as is
        return value

    # Optional configuration for Pydantic settings
    model_config = SettingsConfigDict(env_file=".env")


# Load settings
main = Settings()
