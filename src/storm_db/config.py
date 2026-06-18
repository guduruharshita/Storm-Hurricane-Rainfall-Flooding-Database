from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./storm_events.db"
    api_title: str = "Storm & Natural Disaster Database API"
    api_version: str = "1.0.0"
    debug: bool = False

    model_config = SettingsConfigDict(env_prefix="STORM_", env_file=".env", extra="ignore")


settings = Settings()
