from pydantic import BaseSettings


class Settings(BaseSettings):
    LOCAL_FILE_PATH: str = "C:\\Users\\Michael\\min.io storage\\storage"
    ACCESS_KEY: str = "minioadmin"
    SECRET_KEY: str = "minioadmin"


settings = Settings()
