from pydantic_settings import BaseSettings

class Setting(BaseSettings):
	"""
	Config datas
	"""
    DATABASE_URL: str             # URL for database
    ACCESS_TOKEN_EXPIRE_DAYS: int # For expire day from JWT
    SECRET_KEY:str                # For password JWT
    HESHALGORITHM:str             # Algorithm for hesh JWT

    class Config:
        env_file = ".env"

setting = Setting()
