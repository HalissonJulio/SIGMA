from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str

    # Configuração do pool de conexões
    db_pool_size: int = 5  # conexões que ficam abertas e prontas
    db_max_overflow: int = 5  # conexões extras temporárias sob carga
    db_pool_recycle: int = 1800  # recicla conexões a cada 30 min

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore[call-arg]
