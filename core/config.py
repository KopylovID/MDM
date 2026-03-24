from pydantic import Field, SecretStr
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="UTF-8",
        env_file="./core/.env",
        case_sensitive=False,
    )


class PostgresConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="PG_", extra="ignore")

    host: str
    port: int
    db: str
    user: str
    password: SecretStr


class Config(BaseSettings):
    db: PostgresConfig = Field(default_factory=PostgresConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()
