from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class BotSettings(CommonSettings):
    BOT_TOKEN: str
    WEATHER_API_KEY: str


class DataBaseSettings(CommonSettings):
    model_config = SettingsConfigDict(
        env_prefix="DB_",
    )

    USER: str = "dev_user"
    PASSWORD: str = "dev_user"  # noqa: S105
    HOST: str = "localhost"
    PORT: int = 5432
    NAME: str = "dev_db"
    SCHEMA: str = "main_schema"
    TEST_SCHEMA: str = "test_schema"

    @property
    def URL(self) -> str:  # noqa: N802
        return (
            f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"
        )


class Settings:
    def __init__(self) -> None:
        self.bot = BotSettings()
        self.db = DataBaseSettings()


settings = Settings()
DB_SCHEMA = settings.db.SCHEMA
