from pydantic_settings import BaseSettings
from decouple import config, Config, RepositoryEnv

config = Config(RepositoryEnv(".env"))

class Settings(BaseSettings):
    DS_TOKEN: str = config("DS_TOKEN", default="")
    CHANNEL_ID: str = config("CHANNEL_ID", default="")

settings = Settings()