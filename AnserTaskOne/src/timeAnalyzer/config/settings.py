import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    BASE_URL: str = os.getenv("TIME_API_URL", "https://yandex.com/time/sync.json")
    DEFAULT_GEO: str = os.getenv("DEFAULT_GEO", "213")
    TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "10"))
    RETRY_ATTEMPTS: int = int(os.getenv("RETRY_ATTEMPTS", "3"))
    REQUEST_DELAY: float = float(os.getenv("REQUEST_DELAY", "0.5"))

    @classmethod
    def get_settings(cls) -> "Settings":
        return cls()

settings = Settings.get_settings()