from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = "Event Pipeline"
    debug: bool = True
    max_queue_size: int = 1000


settings = Settings()
