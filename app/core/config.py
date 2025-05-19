from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_DAYS: int
    SECRET_KEY:str
    HESHALGORITHM:str

    class Config:
        env_file = ".env"

setting = Setting()
