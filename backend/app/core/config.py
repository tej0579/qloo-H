import os
from typing import List, Union
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Qloo API config
    QLOO_API_KEY: str = Field(
        default_factory=lambda: os.getenv("QLOO_API_KEY", ""),
        description="Qloo Taste Intelligence API key loaded from the environment"
    )
    QLOO_BASE_URL: str = Field(
        default="https://hackathon.api.qloo.com",
        description="Base URL for Qloo API"
    )

    # Server config
    ENVIRONMENT: str = Field(default="development")
    PORT: int = Field(default=8000)
    HOST: str = Field(default="0.0.0.0")
    CORS_ORIGINS: Union[List[str], str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000", "*"]
    )

    # Optional LLM Key
    OPENAI_API_KEY: str = Field(default="")

    # Request timeouts
    QLOO_TIMEOUT_SECONDS: float = Field(default=15.0)

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        if isinstance(self.CORS_ORIGINS, str):
            import json
            try:
                parsed = json.loads(self.CORS_ORIGINS)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                return [orig.strip() for orig in self.CORS_ORIGINS.split(",") if orig.strip()]
        return ["*"]

settings = Settings()
