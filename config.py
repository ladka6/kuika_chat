from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_HOST: str = Field("localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(5432, env="POSTGRES_PORT")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    REDIS_URL: str = Field(..., env="REDIS_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SESSION_TYPE: str = "filesystem"
    SESSION_PERMANENT: bool = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
